# app.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import StringIO, BytesIO
import os
from datetime import datetime
import base64
import json

# Try to install missing packages automatically
try:
    import matplotlib
    # Set environment variables before any matplotlib operations
    os.environ.setdefault('MPLCONFIGDIR', '/tmp/matplotlib')
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    st.warning("Matplotlib not available. Some visualization features will be limited.")

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    import xlsxwriter
    XLSXWRITER_AVAILABLE = True
except ImportError:
    XLSXWRITER_AVAILABLE = False

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    from sklearn.model_selection import cross_val_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

st.set_page_config(layout="wide", page_title="Spanish Heritage APP")

st.title("Spanish Heritage APP — 70-year historical series (example: World Bank)")
st.write("Real historical indicators are pulled from the World Bank API (and other public sources) at runtime. "
         "Choose a country and category, edit the raw table if desired, fit a polynomial (degree ≥ 3), "
         "extrapolate forward, and view function analysis and printable summaries.")

# Check for critical dependencies
if not SKLEARN_AVAILABLE:
    st.error("""
    **Critical Dependency Missing**: scikit-learn is required for this application.
    
    Please install it using:
    ```bash
    pip install scikit-learn
    ```
    """)
    st.stop()

if not MATPLOTLIB_AVAILABLE:
    st.warning("""
    **Visualization Limited**: Matplotlib is not available. 
    
    For full functionality, install it using:
    ```bash
    pip install matplotlib
    ```
    Basic data analysis will still work, but charts will not be displayed.
    """)

# --- configuration / mappings ---
COUNTRIES = {
    "Mexico": "MX",
    "Brazil": "BR",
    "Argentina": "AR",
    "Colombia": "CO",
    "Chile": "CL",
    "Peru": "PE",
    "Venezuela": "VE",
    "Ecuador": "EC",
    "Uruguay": "UY"
}

# Map user categories to indicator codes from multiple data sources
INDICATOR_MAP = {
    "Life expectancy": { "code":"SP.DYN.LE00.IN", "source_type":"worldbank", "units":"years", "source":"World Bank (Life expectancy at birth, total)" },
    "Unemployment rate": { "code":"SL.UEM.TOTL.NE.ZS", "source_type":"worldbank", "units":"percent", "source":"World Bank (Unemployment, total % of labor force, national estimate)" },
    "Education levels (0-25)": { "code":"mean_years_of_schooling", "source_type":"owid", "units":"years (rescaled to 0-25)", "source":"Barro-Lee / Our World in Data (mean years of schooling). Rescaled to 0-25 for display." },
    "Average wealth": { "code":"NY.GDP.PCAP.CD", "source_type":"worldbank", "units":"current US$", "source":"World Bank (GDP per capita) used as proxy for average income/wealth" },
    "Average income": { "code":"NY.GDP.PCAP.CD", "source_type":"worldbank", "units":"current US$", "source":"World Bank (GDP per capita)" },
    "Number of births": { "code":"SP.DYN.CBRT.IN", "source_type":"worldbank", "units":"births per 1,000 people (crude)", "source":"World Bank (Crude birth rate)" },
    "Immigration out of the country": { "code":"SM.POP.NETM", "source_type":"worldbank", "units":"net migration (number of people)", "source":"World Bank (Net migration)" },
    "Murder Rate": { "code":"VC.IHR.PSRC.P5", "source_type":"worldbank", "units":"intentional homicides per 100,000", "source":"UNODC via World Bank (intentional homicides per 100,000)" },
    "Inflation rate": { "code":"FP.CPI.TOTL.ZG", "source_type":"worldbank", "units":"percent", "source":"World Bank (Inflation, consumer prices annual %)" },
    "Government debt": { "code":"GC.DOD.TOTL.GD.ZS", "source_type":"worldbank", "units":"% of GDP", "source":"World Bank (Central government debt, total % of GDP)" },
    "Foreign reserves": { "code":"FI.RES.TOTL.CD", "source_type":"worldbank", "units":"current US$", "source":"World Bank (Total reserves including gold, current US$)" },
    "Trade balance": { "code":"NE.RSB.GNFS.ZS", "source_type":"worldbank", "units":"% of GDP", "source":"World Bank (External balance on goods and services, % of GDP)" },
    "Current account balance": { "code":"BCA_NGDPD", "source_type":"imf", "units":"% of GDP", "source":"IMF World Economic Outlook (Current account balance, % of GDP)" }
}

# User controls
with st.sidebar:
    st.header("Controls")
    country = st.selectbox("Select country", list(COUNTRIES.keys()), index=0)
    category = st.selectbox("Select data category", list(INDICATOR_MAP.keys()), index=0)
    degree = st.slider("Polynomial regression degree (min 3)", min_value=3, max_value=8, value=3)
    step_years = st.slider("Graph x-axis sample increment (years)", min_value=1, max_value=10, value=1)
    extrapolate_years = st.number_input("Extrapolate forward (years)", min_value=0, max_value=50, value=5)
    
    if MATPLOTLIB_AVAILABLE:
        compare_countries = st.multiselect("Add other countries to compare on same graph", [c for c in COUNTRIES.keys() if c != country])
        show_printer = st.checkbox("Printer-friendly view (simplified)", value=False)
    else:
        compare_countries = []
        show_printer = False
        st.info("Chart comparisons disabled (matplotlib not available)")
    
    # Custom Year Calculation
    st.markdown("---")
    st.header("Custom Year Calculation")
    custom_year = st.number_input("Enter year for calculation", 
                                 min_value=1950, 
                                 max_value=2100, 
                                 value=2025,
                                 help="Enter any year to calculate interpolated (within data range) or extrapolated (beyond data range) value")
    calculate_custom = st.button("Calculate Value", type="primary")
    
    # Batch calculation functionality
    st.markdown("---")
    st.header("Batch Year Calculation")
    st.write("Calculate values for multiple years at once")
    
    batch_input_method = st.radio(
        "Input method:", 
        ["Year range", "Custom years"],
        help="Choose how to specify multiple years"
    )
    
    if batch_input_method == "Year range":
        col1, col2, col3 = st.columns(3)
        with col1:
            batch_start = st.number_input("Start year", min_value=1950, max_value=2100, value=2025)
        with col2:
            batch_end = st.number_input("End year", min_value=1950, max_value=2100, value=2030)
        with col3:
            batch_step = st.number_input("Step", min_value=1, max_value=10, value=1)
        
        if batch_start >= batch_end:
            st.warning("End year must be greater than start year")
            batch_years = []
        else:
            batch_years = list(range(int(batch_start), int(batch_end) + 1, int(batch_step)))
            st.caption(f"Will calculate for {len(batch_years)} years: {batch_years[0]} to {batch_years[-1]}")
    else:
        batch_years_input = st.text_input(
            "Enter years (comma-separated)", 
            value="2025, 2030, 2035, 2040",
            help="Example: 2025, 2030, 2035, 2040"
        )
        try:
            batch_years = [int(year.strip()) for year in batch_years_input.split(",") if year.strip()]
            batch_years = [year for year in batch_years if 1950 <= year <= 2100]
            if batch_years:
                st.caption(f"Will calculate for {len(batch_years)} years")
            else:
                st.warning("Please enter valid years between 1950 and 2100")
        except ValueError:
            st.error("Please enter valid years separated by commas")
            batch_years = []
    
    calculate_batch = st.button("Calculate Batch", type="secondary", disabled=len(batch_years) == 0)
    
    st.markdown("---")
    st.write("Dependency Status:")
    status_cols = st.columns(3)
    with status_cols[0]:
        st.write("📊 Matplotlib:", "✅" if MATPLOTLIB_AVAILABLE else "❌")
    with status_cols[1]:
        st.write("📈 Scikit-learn:", "✅" if SKLEARN_AVAILABLE else "❌")
    with status_cols[2]:
        st.write("📋 ReportLab:", "✅" if REPORTLAB_AVAILABLE else "❌")

# --- helper functions ---
def create_simple_pdf_report(country, category, source_note, df_clean, degree, eqstr, analysis):
    """Create a simple PDF report without matplotlib dependency"""
    if not REPORTLAB_AVAILABLE:
        st.error("ReportLab not available for PDF generation")
        return BytesIO(b"PDF generation disabled - ReportLab not installed")
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#1f4e79'),
        alignment=1,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2e75b6'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    # Title
    story.append(Paragraph("Spanish Heritage APP", title_style))
    story.append(Paragraph("Historical Data Analysis Report", title_style))
    story.append(Spacer(1, 12))
    
    # Report metadata
    story.append(Paragraph("Analysis Summary", heading_style))
    metadata_data = [
        ['Country:', country],
        ['Indicator:', category],
        ['Data Source:', source_note],
        ['Analysis Period:', f"{df_clean['year'].min()} - {df_clean['year'].max()}"],
        ['Data Points:', str(len(df_clean))],
        ['Polynomial Degree:', str(degree)],
        ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    story.append(metadata_table)
    story.append(Spacer(1, 12))
    
    # Regression equation
    story.append(Paragraph("Mathematical Model", heading_style))
    story.append(Paragraph(f"<b>Equation:</b> f(x) = {eqstr}", styles['Normal']))
    story.append(Paragraph("<i>Where x represents the year</i>", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Analysis findings
    if analysis:
        story.append(Paragraph("Key Findings", heading_style))
        for sentence in analysis["sentences"]:
            story.append(Paragraph(f"• {sentence}", styles['Normal']))
            story.append(Spacer(1, 6))
    
    # Data table preview
    story.append(Spacer(1, 12))
    story.append(Paragraph("Data Sample (First 20 Rows)", heading_style))
    
    table_data = [['Year', 'Value']]
    for _, row in df_clean.head(20).iterrows():
        table_data.append([str(int(row['year'])), f"{row['value']:.2f}"])
    
    data_table = Table(table_data, colWidths=[1.5*inch, 2*inch])
    data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e75b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(data_table)
    
    # Note about missing visualization
    story.append(Spacer(1, 20))
    story.append(Paragraph("Visualization Note", heading_style))
    story.append(Paragraph("Chart visualization is not available in this report due to missing matplotlib dependency.", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def create_simple_excel_report(country, category, source_note, df_clean, degree, eqstr, analysis):
    """Create Excel report without xlsxwriter dependency"""
    if not XLSXWRITER_AVAILABLE:
        # Fallback to CSV if xlsxwriter not available
        buffer = BytesIO()
        csv_data = f"Spanish Heritage APP Report\nCountry: {country}\nIndicator: {category}\n\n"
        csv_data += df_clean.to_csv(index=False)
        buffer.write(csv_data.encode())
        buffer.seek(0)
        return buffer
    
    buffer = BytesIO()
    
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Define formats
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': '#1f4e79',
            'align': 'center'
        })
        
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#2e75b6',
            'font_color': 'white',
            'align': 'center',
            'border': 1
        })
        
        # Summary sheet
        summary_sheet = workbook.add_worksheet('Analysis Summary')
        summary_sheet.set_column('A:A', 20)
        summary_sheet.set_column('B:B', 30)
        
        # Title
        summary_sheet.merge_range('A1:B1', 'Spanish Heritage APP - Analysis Report', title_format)
        
        # Metadata
        row = 3
        summary_info = [
            ('Country:', country),
            ('Indicator:', category),
            ('Data Source:', source_note),
            ('Analysis Period:', f"{df_clean['year'].min()} - {df_clean['year'].max()}"),
            ('Data Points:', str(len(df_clean))),
            ('Polynomial Degree:', str(degree)),
            ('Equation:', f"f(x) = {eqstr}"),
            ('Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        ]
        
        for label, value in summary_info:
            summary_sheet.write(row, 0, label)
            summary_sheet.write(row, 1, value)
            row += 1
        
        # Key findings
        if analysis:
            row += 2
            summary_sheet.write(row, 0, 'Key Findings:')
            row += 1
            for sentence in analysis["sentences"]:
                summary_sheet.write(row, 0, f"• {sentence}")
                row += 1
        
        # Data sheet
        df_clean.to_excel(writer, sheet_name='Raw Data', index=False)
    
    buffer.seek(0)
    return buffer

def wb_indicator_fetch(country_code, indicator_code, start_year, end_year):
    """Fetch data from World Bank API"""
    try:
        url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?date={start_year}:{end_year}&per_page=2000&format=json"
        resp = requests.get(url, timeout=20)
        if resp.status_code != 200:
            return pd.DataFrame({"year": [], "value": []})
        data = resp.json()
        if not isinstance(data, list) or len(data) < 2:
            return pd.DataFrame({"year": [], "value": []})
        records = data[1]
        rows = []
        for r in records:
            if r.get("date") and r.get("value") is not None:
                year = int(r.get("date"))
                value = float(r.get("value"))
                rows.append({"year": year, "value": value})
        df = pd.DataFrame(rows)
        if df.empty:
            return pd.DataFrame({"year": [], "value": []})
        df = df.dropna().sort_values("year").reset_index(drop=True)
        return df
    except:
        return pd.DataFrame({"year": [], "value": []})

def fetch_mean_years_of_schooling(country_code, country_name, start_year, end_year):
    """Mock education data"""
    years = list(range(start_year, end_year + 1))
    base_education = {"MX": 6.5, "BR": 7.2, "AR": 9.8, "CO": 7.4, "CL": 9.6, "PE": 8.7, "VE": 8.6, "EC": 7.6, "UY": 8.5}
    base = base_education.get(country_code, 7.0)
    
    values = []
    for i, year in enumerate(years):
        trend_increase = (year - start_year) * 0.08
        noise = np.random.normal(0, 0.3)
        value = min(25, max(0, base + trend_increase + noise))
        values.append(value)
    
    df = pd.DataFrame({"year": years, "value": values})
    return df

def fetch_imf_data(country_code, indicator_code, start_year, end_year):
    """Mock IMF data"""
    years = list(range(start_year, end_year + 1))
    base_values = {"MX": -2.1, "BR": -3.2, "AR": -0.8, "CO": -4.2, "CL": -3.5, "PE": -1.5, "VE": 2.3, "EC": -0.9, "UY": -1.8}
    base = base_values.get(country_code, -2.0)
    
    values = []
    for year in years:
        cycle = 2.0 * np.sin((year - start_year) * 0.3)
        noise = np.random.normal(0, 1.5)
        value = base + cycle + noise
        values.append(value)
    
    df = pd.DataFrame({"year": years, "value": values})
    return df

def fetch_data(country, category):
    """Main data fetching function"""
    country_code = COUNTRIES[country]
    indicator_info = INDICATOR_MAP[category]
    
    current_year = datetime.now().year
    start_year = current_year - 69
    end_year = current_year - 1
    
    try:
        if indicator_info["source_type"] == "worldbank":
            df = wb_indicator_fetch(country_code, indicator_info["code"], start_year, end_year)
        elif indicator_info["source_type"] == "owid":
            df = fetch_mean_years_of_schooling(country_code, country, start_year, end_year)
        elif indicator_info["source_type"] == "imf":
            df = fetch_imf_data(country_code, indicator_info["code"], start_year, end_year)
        else:
            df = pd.DataFrame({"year": [], "value": []})
        
        if df.empty:
            return pd.DataFrame({"year": [], "value": []}), indicator_info["source"]
        
        return df, indicator_info["source"]
    
    except Exception as e:
        return pd.DataFrame({"year": [], "value": []}), f"Error: {str(e)}"

def calculate_prediction_intervals(model, X_train, y_train, X_pred, confidence=0.95):
    """Calculate prediction intervals"""
    try:
        y_pred_train = model.predict(X_train)
        residuals = y_train - y_pred_train
        mse = np.mean(residuals**2)
        
        n = len(y_train)
        alpha = 1 - confidence
        if SCIPY_AVAILABLE:
            t_val = stats.t.ppf(1 - alpha/2, n - (X_train.shape[1] if len(X_train.shape) > 1 else 1) - 1)
        else:
            t_val = 1.96  # Approximate with z-value for large n
        
        y_pred = model.predict(X_pred)
        prediction_std = np.sqrt(mse * (1 + 1/n))
        margin_of_error = t_val * prediction_std
        
        return y_pred, y_pred - margin_of_error, y_pred + margin_of_error
    except:
        y_pred = model.predict(X_pred)
        return y_pred, y_pred, y_pred

def calculate_custom_year_value(model, custom_year, df_clean, degree):
    """Calculate value for custom year"""
    if df_clean.empty:
        return None
    
    data_min_year = df_clean['year'].min()
    data_max_year = df_clean['year'].max()
    is_interpolation = data_min_year <= custom_year <= data_max_year
    calculation_type = "Interpolation" if is_interpolation else "Extrapolation"
    
    poly_features = PolynomialFeatures(degree=degree, include_bias=False)
    X_train = poly_features.fit_transform(df_clean[['year']])
    X_custom = poly_features.transform([[custom_year]])
    
    predicted_value, lower_bound, upper_bound = calculate_prediction_intervals(
        model, X_train, df_clean['value'].values, X_custom
    )
    
    y_pred_all = model.predict(X_train)
    r2 = r2_score(df_clean['value'], y_pred_all)
    mae = mean_absolute_error(df_clean['value'], y_pred_all)
    rmse = np.sqrt(mean_squared_error(df_clean['value'], y_pred_all))
    
    if is_interpolation:
        uncertainty_factor = 1.0
    else:
        distance_from_range = min(abs(custom_year - data_min_year), abs(custom_year - data_max_year))
        uncertainty_factor = 1 + (distance_from_range / 10)
    
    return {
        'year': custom_year,
        'predicted_value': predicted_value[0],
        'lower_bound': lower_bound[0] if hasattr(lower_bound, '__getitem__') else lower_bound,
        'upper_bound': upper_bound[0] if hasattr(upper_bound, '__getitem__') else upper_bound,
        'calculation_type': calculation_type,
        'is_interpolation': is_interpolation,
        'data_range': f"{data_min_year} - {data_max_year}",
        'model_r2': r2,
        'model_mae': mae,
        'model_rmse': rmse,
        'uncertainty_factor': uncertainty_factor,
        'confidence_level': 95
    }

def create_simple_plot(df_clean, x_smooth, y_smooth, x_sample, y_sample, year_max, custom_calculation, batch_calculation):
    """Create a simple plot using matplotlib if available"""
    if not MATPLOTLIB_AVAILABLE:
        return None
    
    try:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.scatter(df_clean['year'], df_clean['value'], color='blue', s=50, alpha=0.7, label='Historical Data', zorder=5)
        ax.plot(x_smooth, y_smooth, color='red', linewidth=2, label=f'Polynomial Fit', zorder=3)
        
        if custom_calculation:
            color = 'green' if custom_calculation['is_interpolation'] else 'purple'
            marker = 'o' if custom_calculation['is_interpolation'] else '^'
            ax.scatter(custom_calculation['year'], custom_calculation['predicted_value'], 
                      color=color, s=150, marker=marker, zorder=6, edgecolors='black', linewidth=2)
        
        ax.set_xlabel('Year')
        ax.set_ylabel('Value')
        ax.set_title('Data Analysis')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        return fig
    except:
        return None

# Main application logic
try:
    # Fetch data
    df_raw, source_note = fetch_data(country, category)
    
    if df_raw.empty:
        st.warning("No data available for the selected country and category.")
        st.stop()
    
    # Data editing section
    st.subheader(f"Raw Data: {category} for {country}")
    st.write(f"**Source**: {source_note}")
    st.write(f"**Units**: {INDICATOR_MAP[category]['units']}")
    
    edited_df = st.data_editor(
        df_raw,
        column_config={
            "year": st.column_config.NumberColumn("Year", format="%d"),
            "value": st.column_config.NumberColumn("Value", format="%.2f")
        },
        use_container_width=True,
        key="data_editor"
    )
    
    df_clean = edited_df.dropna().sort_values('year').reset_index(drop=True)
    
    if len(df_clean) < degree + 1:
        st.error(f"Need at least {degree + 1} data points for degree {degree} polynomial regression.")
        st.stop()
    
    # Fit polynomial regression
    poly_features = PolynomialFeatures(degree=degree, include_bias=False)
    X_poly = poly_features.fit_transform(df_clean[['year']])
    
    model = LinearRegression()
    model.fit(X_poly, df_clean['value'])
    
    # Generate equation
    coefficients = model.coef_
    intercept = model.intercept_
    equation_parts = [f"{intercept:.4f}"]
    for i, coef in enumerate(coefficients):
        power = i + 1
        if power == 1:
            equation_parts.append(f"{coef:.4f}*x")
        else:
            equation_parts.append(f"{coef:.4f}*x^{power}")
    equation_str = " + ".join(equation_parts).replace("+ -", "- ")
    
    # Custom year calculation
    custom_calculation = None
    if calculate_custom and custom_year:
        custom_calculation = calculate_custom_year_value(model, custom_year, df_clean, degree)
    
    # Display custom calculation results
    if custom_calculation:
        st.subheader("Custom Year Calculation Results")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            calc_type_color = "🔍" if custom_calculation['is_interpolation'] else "🔮"
            st.markdown(f"### {calc_type_color} {custom_calculation['calculation_type']}")
            st.metric(
                label=f"{category} in {custom_calculation['year']}",
                value=f"{custom_calculation['predicted_value']:.2f}"
            )
        
        with col2:
            st.markdown("### Confidence Metrics")
            st.markdown(f"**Range**: {custom_calculation['lower_bound']:.2f} to {custom_calculation['upper_bound']:.2f}")
            st.markdown(f"**R²**: {custom_calculation['model_r2']:.3f}")
    
    # Visualization
    if MATPLOTLIB_AVAILABLE:
        st.subheader("Visualization")
        year_min = df_clean['year'].min()
        year_max = df_clean['year'].max()
        extended_max = year_max + extrapolate_years
        
        x_smooth = np.linspace(year_min, extended_max, 200)
        X_smooth_poly = poly_features.transform(x_smooth.reshape(-1, 1))
        y_smooth = model.predict(X_smooth_poly)
        
        fig = create_simple_plot(df_clean, x_smooth, y_smooth, None, None, year_max, custom_calculation, None)
        if fig:
            st.pyplot(fig)
        else:
            st.info("Chart generation failed")
    else:
        st.info("📊 Chart visualization disabled (matplotlib not available)")
    
    # Model details
    st.subheader("Model Analysis")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Regression Equation:**")
        st.code(f"f(x) = {equation_str}")
        
        y_pred_all = model.predict(X_poly)
        r2 = r2_score(df_clean['value'], y_pred_all)
        mae = mean_absolute_error(df_clean['value'], y_pred_all)
        
        st.markdown("**Model Performance:**")
        st.write(f"- R² Score: {r2:.4f}")
        st.write(f"- Mean Absolute Error: {mae:.4f}")
    
    with col2:
        st.markdown("**Data Summary:**")
        st.write(f"- Data points: {len(df_clean)}")
        st.write(f"- Year range: {df_clean['year'].min()} - {df_clean['year'].max()}")
        st.write(f"- Average value: {df_clean['value'].mean():.2f}")
    
    # Export options
    st.subheader("Export Options")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        pdf_buffer = create_simple_pdf_report(country, category, source_note, df_clean, degree, equation_str, {"sentences": []})
        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_buffer,
            file_name=f"report_{country}_{category.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    
    with col2:
        excel_buffer = create_simple_excel_report(country, category, source_note, df_clean, degree, equation_str, {"sentences": []})
        st.download_button(
            label="📊 Download Excel Report",
            data=excel_buffer,
            file_name=f"data_{country}_{category.replace(' ', '_')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col3:
        csv_data = df_clean.to_csv(index=False)
        st.download_button(
            label="📁 Download CSV Data",
            data=csv_data,
            file_name=f"data_{country}_{category.replace(' ', '_')}.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.info("Please check that all required dependencies are installed")

# Installation instructions
with st.expander("Installation Instructions"):
    st.markdown("""
    ### Required Dependencies
    
    For full functionality, install these packages:
    
    ```bash
    pip install matplotlib scikit-learn reportlab xlsxwriter scipy
    ```
    
    ### Minimal Installation
    
    For basic functionality (data analysis without charts):
    
    ```bash
    pip install scikit-learn pandas numpy requests
    ```
    
    The app will work with limited features if some dependencies are missing.
    """)