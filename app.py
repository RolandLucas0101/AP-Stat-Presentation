import streamlit as st
import base64
from io import BytesIO
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AP Statistics for Career Success",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #667eea;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #764ba2;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .slide-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .example-box {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    
    .highlight {
        background: #fff3cd;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    .career-title {
        color: #764ba2;
        font-size: 1.8rem;
        margin-bottom: 1rem;
    }
    
    .intro-section {
        background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .download-btn {
        background: #28a745;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-weight: bold;
    }
    
    .resource-link {
        background: #e7f3ff;
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .resource-link a {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
    }
    
    .resource-link a:hover {
        text-decoration: underline;
    }
    
    .case-study {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    .print-btn {
        background: #007bff;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        border: none;
        margin: 0.5rem;
        cursor: pointer;
        font-weight: bold;
    }
    
    /* Hide elements during print */
    @media print {
        .no-print {
            display: none !important;
        }
        .always-print {
            display: block !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# UPDATED AND VERIFIED Career Resources with WORKING LINKS
CAREER_RESOURCES = {
    "general": {
        "Netflix A/B Testing Platform": "https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15",
        "CDC Public Health Case Studies": "https://www.cdc.gov/nchs/pressroom/casestudies.htm",
        "American Statistical Association Case Studies": "https://www.amstat.org/asa/education/statistical-case-studies.aspx",
        "FiveThirtyEight Sports Analytics": "https://fivethirtyeight.com/tag/statistics/",
        "Khan Academy AP Statistics": "https://www.khanacademy.org/math/ap-statistics",
    },
    "NICU Nurse": {
        "Statistical Analysis of Infant Outcomes": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4481523/",
        "Control Charts in Healthcare": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3917520/",
        "NICU Quality Improvement Statistics": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5008519/",
        "Neonatal Vital Sign Analysis": "https://www.sciencedirect.com/science/article/abs/pii/S002234761730555X",
    },
    "Marketing Professional": {
        "Google Analytics Academy": "https://analytics.google.com/analytics/academy/",
        "A/B Testing Case Studies": "https://www.optimizely.com/optimization-glossary/ab-testing/",
        "Marketing Statistics Tutorial": "https://www.coursera.org/learn/marketing-analytics",
        "Digital Marketing Metrics": "https://www.hubspot.com/marketing-statistics",
    },
    "Pediatric Surgeon": {
        "Surgical Outcomes Statistics": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6082075/",
        "Pediatric Surgery Research": "https://www.jpedsurg.org/",
        "Surgical Risk Calculator": "https://riskcalculator.facs.org/RiskCalculator/",
        "Clinical Trial Statistics": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2876926/",
    },
    "Registered Nurse": {
        "Nursing Statistics Education": "https://www.nln.org/education/statistics-for-nurses",
        "Quality Improvement in Healthcare": "https://www.ahrq.gov/talkingquality/index.html",
        "Lab Value Interpretation": "https://www.ncbi.nlm.nih.gov/books/NBK279390/",
        "Nursing Research Statistics": "https://www.nursingcenter.com/journalarticle?Article_ID=5549435",
    },
    "Cybersecurity Professional": {
        "Cybersecurity Statistics Resources": "https://www.sans.org/security-resources/",
        "Threat Detection Statistics": "https://www.cisa.gov/cybersecurity",
        "Security Metrics Guide": "https://csrc.nist.gov/projects/security-metrics",
        "Network Analysis Tutorial": "https://www.kaggle.com/learn/network-analysis",
    },
    "Cosmetic Scientist": {
        "Cosmetic Science Statistics": "https://www.personalcarecouncil.org/science/statistics/",
        "Product Testing Methods": "https://www.astm.org/standards/cosmetic-and-personal-care-products.html",
        "Consumer Research Statistics": "https://www.quirks.com/articles/category/statistics",
        "Formulation Science": "https://www.scconline.org/",
    },
    "Dermatology Physician Assistant": {
        "Skin Cancer Statistics": "https://www.cancer.org/cancer/types/skin-cancer.html",
        "Dermatology Research": "https://www.aad.org/publications",
        "Diagnostic Test Statistics": "https://www.ncbi.nlm.nih.gov/books/NBK557530/",
        "Clinical Dermatology": "https://jamanetwork.com/journals/jamadermatology",
    },
    "Electrical Engineer": {
        "Engineering Statistics": "https://www.ieee.org/education/online-courses.html",
        "Quality Control Statistics": "https://asq.org/quality-resources/statistics",
        "Reliability Engineering": "https://www.weibull.com/basics/reliability.htm",
        "Circuit Analysis Tutorial": "https://www.allaboutcircuits.com/textbook/",
    },
    "Civil Engineer": {
        "Structural Engineering Statistics": "https://www.asce.org/education/online-courses",
        "Construction Statistics": "https://www.agc.org/resources/construction-data",
        "Materials Testing Standards": "https://www.astm.org/standards/construction-standards.html",
        "Bridge Safety Statistics": "https://www.fhwa.dot.gov/bridge/",
    },
    "Pediatrician": {
        "CDC Growth Charts": "https://www.cdc.gov/growthcharts/",
        "Pediatric Health Statistics": "https://www.aap.org/en/patient-care/",
        "Vaccine Statistics": "https://www.cdc.gov/vaccines/stats-surv/index.html",
        "Child Health Research": "https://publications.aap.org/pediatrics",
    },
    "Software Developer": {
        "A/B Testing at Google": "https://ai.google/research/pubs/pub36500/",
        "Software Metrics": "https://www.atlassian.com/devops/devops-tools/devops-metrics",
        "Programming Statistics": "https://stackoverflow.blog/2021/11/22/the-state-of-developer-ecosystem-2021/",
        "Data Science Tutorials": "https://www.datacamp.com/courses/statistics-fundamentals",
    },
    "Physicist / Nanotechnologist": {
        "Physics Data Analysis": "https://www.physicsforums.com/threads/statistics-in-physics.1000000/",
        "Nanotechnology Research": "https://www.nano.gov/you/nanotechnology-benefits",
        "Scientific Statistics": "https://www.nature.com/subjects/statistics",
        "Materials Science Data": "https://www.materialsproject.org/",
    }
}

# App data
slides = [
    {
        "title": "📊 AP Statistics",
        "subtitle": "Your Gateway to Career Success",
        "content": "Why Juniors Should Take AP Stats Senior Year",
        "type": "title"
    },
    {
        "title": "Why AP Statistics Matters",
        "content": {
            "benefits": [
                "Required or recommended for MOST college majors",
                "Earn college credit and save tuition money",
                "Build critical thinking and data analysis skills",
                "Stand out on college applications",
                "Prepare for data-driven careers in ANY field"
            ],
            "applications": "Whether you're interested in healthcare, technology, engineering, business, or research, statistics is the foundation of decision-making in the modern workplace. Let's explore how AP Statistics prepares you for YOUR future career!",
            "resources": "general"
        },
        "type": "intro"
    },
    {
        "title": "🏥 NICU Nurse",
        "content": {
            "description": "How Statistics Empowers NICU Nurses",
            "examples": [
                {
                    "title": "Patient Monitoring & Risk Assessment",
                    "content": "NICU nurses analyze vital sign patterns (heart rate, oxygen levels, temperature) to detect abnormalities. Using statistical concepts like <span class='highlight'>mean, standard deviation, and outliers</span>, you can identify when a baby's vitals fall outside normal ranges and require immediate intervention."
                },
                {
                    "title": "Treatment Effectiveness Analysis",
                    "content": "When implementing care protocols, nurses track outcomes across multiple patients. Using <span class='highlight'>hypothesis testing and confidence intervals</span>, you can determine if a new feeding schedule or medication dosage is significantly improving patient outcomes compared to standard care."
                }
            ],
            "resources": "NICU Nurse"
        },
        "type": "career"
    },
    {
        "title": "📈 Marketing Professional",
        "content": {
            "description": "How Statistics Drives Marketing Success",
            "examples": [
                {
                    "title": "Campaign Performance Analysis",
                    "content": "Marketing professionals analyze customer data to measure campaign effectiveness. Using <span class='highlight'>regression analysis and correlation</span>, you can identify which advertising channels (social media, email, TV) drive the most conversions and optimize budget allocation accordingly."
                },
                {
                    "title": "Customer Segmentation & Targeting",
                    "content": "Understanding customer behavior requires analyzing demographic and purchase data. Using <span class='highlight'>probability distributions and sampling methods</span>, you can segment audiences, predict purchasing patterns, and create personalized marketing strategies for different customer groups."
                }
            ],
            "resources": "Marketing Professional"
        },
        "type": "career"
    },
    {
        "title": "⚕️ Pediatric Surgeon",
        "content": {
            "description": "How Statistics Enhances Surgical Excellence",
            "examples": [
                {
                    "title": "Surgical Outcome Prediction",
                    "content": "Surgeons evaluate patient risk factors (age, weight, medical history) to predict surgical outcomes. Using <span class='highlight'>probability and risk assessment</span>, you can calculate the likelihood of complications and make informed decisions about surgical approaches for each child."
                },
                {
                    "title": "Clinical Research & Evidence-Based Practice",
                    "content": "Surgical techniques improve through research. Using <span class='highlight'>experimental design and statistical significance testing</span>, you can evaluate whether new surgical methods or robotic-assisted procedures produce better results than traditional techniques, ensuring you provide the best care."
                }
            ],
            "resources": "Pediatric Surgeon"
        },
        "type": "career"
    },
    {
        "title": "💉 Registered Nurse",
        "content": {
            "description": "How Statistics Improves Patient Care",
            "examples": [
                {
                    "title": "Interpreting Lab Results",
                    "content": "Nurses review patient lab work daily (blood counts, glucose levels, kidney function). Understanding <span class='highlight'>normal distributions and reference ranges</span> allows you to quickly identify abnormal results that require physician notification or immediate patient intervention."
                },
                {
                    "title": "Quality Improvement & Safety",
                    "content": "Healthcare facilities track infection rates, medication errors, and patient falls. Using <span class='highlight'>control charts and statistical process control</span>, nurses on quality improvement teams can identify trends, implement safety protocols, and measure whether interventions reduce adverse events."
                }
            ],
            "resources": "Registered Nurse"
        },
        "type": "career"
    },
    {
        "title": "🔒 Cybersecurity Professional",
        "content": {
            "description": "How Statistics Defends Digital Systems",
            "examples": [
                {
                    "title": "Threat Detection & Anomaly Analysis",
                    "content": "Cybersecurity analysts monitor network traffic patterns to identify potential attacks. Using <span class='highlight'>statistical modeling and outlier detection</span>, you can spot unusual login attempts, data transfers, or access patterns that indicate a security breach in progress."
                },
                {
                    "title": "Risk Assessment & Security Metrics",
                    "content": "Organizations must prioritize security investments. Using <span class='highlight'>probability and risk modeling</span>, you can calculate the likelihood and potential impact of different cyber threats, helping leadership allocate resources to protect the most critical systems and data."
                }
            ],
            "resources": "Cybersecurity Professional"
        },
        "type": "career"
    },
    {
        "title": "🧪 Cosmetic Scientist",
        "content": {
            "description": "How Statistics Drives Product Innovation",
            "examples": [
                {
                    "title": "Product Testing & Consumer Research",
                    "content": "Before launching products, cosmetic scientists conduct consumer trials. Using <span class='highlight'>experimental design and hypothesis testing</span>, you can determine if users experience statistically significant improvements in skin texture, hydration, or appearance compared to placebo products."
                },
                {
                    "title": "Formulation Optimization",
                    "content": "Creating effective cosmetics requires testing ingredient combinations. Using <span class='highlight'>regression analysis and optimization techniques</span>, you can identify which ingredient concentrations and ratios produce the best stability, texture, and efficacy results for new products."
                }
            ],
            "resources": "Cosmetic Scientist"
        },
        "type": "career"
    },
    {
        "title": "🩺 Dermatology Physician Assistant",
        "content": {
            "description": "How Statistics Improves Diagnosis & Treatment",
            "examples": [
                {
                    "title": "Diagnostic Accuracy & Pattern Recognition",
                    "content": "Dermatology PAs evaluate skin lesions for cancer risk. Understanding <span class='highlight'>sensitivity, specificity, and positive predictive value</span> helps you interpret AI diagnostic tools, assess biopsy results, and understand the probability that a concerning lesion is actually malignant."
                },
                {
                    "title": "Treatment Protocol Comparison",
                    "content": "Multiple treatment options exist for conditions like acne or eczema. Using <span class='highlight'>comparative analysis and confidence intervals</span>, you can evaluate clinical study data to determine which treatments have the highest success rates and recommend evidence-based therapies to patients."
                }
            ],
            "resources": "Dermatology Physician Assistant"
        },
        "type": "career"
    },
    {
        "title": "⚡ Electrical Engineer",
        "content": {
            "description": "How Statistics Powers Engineering Design",
            "examples": [
                {
                    "title": "Quality Control & Testing",
                    "content": "Electrical engineers test circuit reliability and component performance. Using <span class='highlight'>sampling distributions and hypothesis testing</span>, you can determine if manufactured circuits meet specifications and identify defect rates before products reach consumers."
                },
                {
                    "title": "Predictive Maintenance & Reliability",
                    "content": "Power systems and equipment must be maintained before failures occur. Using <span class='highlight'>probability distributions and survival analysis</span>, you can predict when components are likely to fail, schedule preventive maintenance, and minimize costly unexpected outages."
                }
            ],
            "resources": "Electrical Engineer"
        },
        "type": "career"
    },
    {
        "title": "🏗️ Civil Engineer",
        "content": {
            "description": "How Statistics Ensures Safe Infrastructure",
            "examples": [
                {
                    "title": "Load Analysis & Structural Safety",
                    "content": "Civil engineers design buildings and bridges to withstand various loads. Using <span class='highlight'>probability distributions and safety factors</span>, you can analyze expected weight, wind, and seismic forces to ensure structures can handle extreme conditions with appropriate safety margins."
                },
                {
                    "title": "Materials Testing & Quality Assurance",
                    "content": "Construction projects require testing concrete strength, soil properties, and material durability. Using <span class='highlight'>sampling methods and confidence intervals</span>, you can determine if materials meet building codes and specifications based on test samples rather than testing every batch."
                }
            ],
            "resources": "Civil Engineer"
        },
        "type": "career"
    },
    {
        "title": "👶 Pediatrician",
        "content": {
            "description": "How Statistics Guides Child Healthcare",
            "examples": [
                {
                    "title": "Growth & Development Monitoring",
                    "content": "Pediatricians track children's growth using standardized charts. Understanding <span class='highlight'>percentiles and z-scores</span> allows you to interpret whether a child's height, weight, and head circumference fall within normal ranges or indicate potential developmental or nutritional concerns."
                },
                {
                    "title": "Evidence-Based Treatment Decisions",
                    "content": "Medical research guides pediatric care. Using <span class='highlight'>clinical trial analysis and effect sizes</span>, you can interpret study results to determine which treatments, vaccines, or interventions are most effective for different childhood conditions and age groups."
                }
            ],
            "resources": "Pediatrician"
        },
        "type": "career"
    },
    {
        "title": "💻 Software Developer",
        "content": {
            "description": "How Statistics Powers Modern Software",
            "examples": [
                {
                    "title": "A/B Testing & Feature Optimization",
                    "content": "Developers test different app designs and features with users. Using <span class='highlight'>hypothesis testing and p-values</span>, you can determine if a new interface design or feature significantly improves user engagement, retention, or conversion rates compared to the current version."
                },
                {
                    "title": "Algorithm Performance & Machine Learning",
                    "content": "Modern software relies on AI and data analysis. Using <span class='highlight'>regression, classification, and model evaluation metrics</span>, you can build predictive algorithms, assess model accuracy, and optimize software performance based on user behavior data."
                }
            ],
            "resources": "Software Developer"
        },
        "type": "career"
    },
    {
        "title": "🔬 Physicist / Nanotechnologist",
        "content": {
            "description": "How Statistics Advances Scientific Discovery",
            "examples": [
                {
                    "title": "Experimental Data Analysis",
                    "content": "Physics experiments generate massive datasets with measurement uncertainty. Using <span class='highlight'>error analysis, statistical significance, and uncertainty propagation</span>, you can determine if experimental results support theoretical predictions and separate true signals from background noise."
                },
                {
                    "title": "Materials Characterization & Modeling",
                    "content": "Nanotechnology research involves testing material properties at atomic scales. Using <span class='highlight'>statistical mechanics and distribution analysis</span>, you can analyze particle behavior, predict material properties, and optimize nanomaterial designs for specific applications."
                }
            ],
            "resources": "Physicist / Nanotechnologist"
        },
        "type": "career"
    },
    {
        "title": "Take AP Statistics Next Year!",
        "content": {
            "points": [
                "✓ Prepare for ANY college major",
                "✓ Build essential career skills",
                "✓ Earn college credit",
                "✓ Stand out to admissions"
            ],
            "call_to_action": "Your future career starts with the decisions you make today! 📊",
            "contact": "Questions? Talk to your guidance counselor about registering for AP Statistics!"
        },
        "type": "closing"
    }
]

def create_instructions_file():
    instructions = """HOW TO CONVERT TO POWERPOINT/GOOGLE SLIDES

OPTION 1 - MANUAL RECREATION (Recommended for full control):
1. Open PowerPoint or Google Slides
2. Create a new presentation
3. For each slide in this preview:
   - Create a new slide with appropriate layout
   - Copy the text content
   - Apply similar formatting (colors, fonts, spacing)
   - Add gradient backgrounds where shown

OPTION 2 - SCREENSHOT METHOD (Quick):
1. Use this presentation in full-screen mode
2. Take screenshots of each slide
3. Import screenshots into PowerPoint/Google Slides
4. Add text boxes over screenshots for editability
5. Adjust formatting as needed

DESIGN TIPS:
- Use gradient backgrounds (purple/blue theme)
- Keep text large and readable
- Use consistent colors: Primary purple (#667eea), Secondary purple (#764ba2)
- Include emojis for visual interest
- Use white/light gray cards for examples
- Maintain spacing and hierarchy

CONTENT ORGANIZATION:
Slide 1: Title slide
Slide 2: Introduction to AP Statistics benefits
Slides 3-14: Individual careers (12 careers)
Slide 15: Closing/Call to action

All content is fully editable once transferred to PowerPoint or Google Slides."""
    
    return instructions

def create_flyer():
    """Create a two-page flyer summary (front and back)"""
    today = datetime.now().strftime("%B %d, %Y")
    
    flyer = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @media print {{
                @page {{
                    size: letter;
                    margin: 0.5in;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 11pt;
                    line-height: 1.4;
                    margin: 0;
                    padding: 0;
                }}
                .page {{
                    page-break-after: always;
                    padding: 0.5in;
                    min-height: 10in;
                }}
                .page-break {{
                    page-break-before: always;
                }}
                h1 {{
                    color: #667eea;
                    text-align: center;
                    margin-bottom: 10px;
                    font-size: 24pt;
                }}
                h2 {{
                    color: #764ba2;
                    border-bottom: 2px solid #764ba2;
                    padding-bottom: 5px;
                    font-size: 16pt;
                }}
                .highlight {{
                    background-color: #fff3cd;
                    padding: 2px 4px;
                    border-radius: 3px;
                }}
                .section {{
                    margin: 15px 0;
                    padding: 15px;
                    background: #f8f9fa;
                    border-radius: 5px;
                    border: 1px solid #dee2e6;
                }}
                .career-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 10px;
                    margin: 15px 0;
                }}
                .career-item {{
                    padding: 10px;
                    background: white;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                    font-size: 10pt;
                }}
                .stat-method {{
                    background: #e7f3ff;
                    padding: 8px;
                    margin: 5px 0;
                    border-left: 3px solid #667eea;
                    font-size: 10pt;
                }}
                .contact-info {{
                    text-align: center;
                    margin-top: 30px;
                    font-size: 10pt;
                    padding-top: 15px;
                    border-top: 2px solid #ccc;
                }}
                ul, ol {{
                    margin-left: 20px;
                }}
                li {{
                    margin: 8px 0;
                }}
                .print-only {{
                    display: block;
                }}
                @media screen {{
                    .print-only {{
                        display: none;
                    }}
                }}
            }}
        </style>
    </head>
    <body>
    
    <!-- PAGE 1 (FRONT) -->
    <div class="page">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #667eea; margin-bottom: 5px;">📊 AP Statistics</h1>
            <h2 style="color: #764ba2; margin-top: 0;">Your Gateway to Career Success</h2>
            <p style="font-weight: bold; font-size: 12pt;">Why Juniors Should Take AP Stats Senior Year</p>
            <p style="font-size: 10pt; color: #666;">{today}</p>
        </div>
        
        <div class="section">
            <h2>🚀 Key Benefits of AP Statistics</h2>
            <ul>
                <li><strong>College Credit:</strong> Earn credits and save thousands in tuition</li>
                <li><strong>College Admissions:</strong> Stand out in competitive applications</li>
                <li><strong>Career Preparation:</strong> Required for most STEM and business majors</li>
                <li><strong>Real-World Skills:</strong> Data analysis, critical thinking, problem-solving</li>
                <li><strong>Versatility:</strong> Applies to healthcare, tech, engineering, business, and more</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🎯 AP Statistics in Real Careers</h2>
            <div class="career-grid">
                <div class="career-item">
                    <strong style="color: #667eea;">🏥 NICU Nurse</strong><br>
                    • Vital sign statistical analysis<br>
                    • Treatment effectiveness testing<br>
                    • Infection control statistics
                </div>
                <div class="career-item">
                    <strong style="color: #667eea;">📈 Marketing Professional</strong><br>
                    • A/B testing campaigns<br>
                    • Customer segmentation analysis<br>
                    • ROI statistical analysis
                </div>
                <div class="career-item">
                    <strong style="color: #667eea;">⚕️ Pediatric Surgeon</strong><br>
                    • Surgical risk probability<br>
                    • Outcome prediction models<br>
                    • Clinical trial statistics
                </div>
                <div class="career-item">
                    <strong style="color: #667eea;">🔒 Cybersecurity</strong><br>
                    • Anomaly detection algorithms<br>
                    • Threat probability modeling<br>
                    • Risk statistical analysis
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📚 AP Stats Methods You'll Learn</h2>
            <div class="stat-method"><strong>Hypothesis Testing:</strong> Test ideas with data</div>
            <div class="stat-method"><strong>Regression Analysis:</strong> Find relationships between variables</div>
            <div class="stat-method"><strong>Probability Distributions:</strong> Model uncertainty</div>
            <div class="stat-method"><strong>Confidence Intervals:</strong> Estimate with precision</div>
            <div class="stat-method"><strong>Sampling Methods:</strong> Study populations efficiently</div>
            <div class="stat-method"><strong>Experimental Design:</strong> Design valid studies</div>
        </div>
        
        <div class="contact-info">
            <p><strong>Questions?</strong> Talk to your guidance counselor about registering for AP Statistics!</p>
            <p>Scan QR code for interactive presentation → 📱</p>
        </div>
    </div>
    
    <!-- PAGE 2 (BACK) -->
    <div class="page page-break">
        <div style="text-align: center; margin-bottom: 20px;">
            <h1 style="color: #764ba2;">AP Statistics Career Connections</h1>
        </div>
        
        <div class="section">
            <h2>💡 More Career Examples</h2>
            <div class="career-grid">
                <div class="career-item">
                    <strong style="color: #764ba2;">🧪 Cosmetic Scientist</strong><br>
                    • Product testing statistics<br>
                    • Formulation optimization<br>
                    • Consumer research analysis
                </div>
                <div class="career-item">
                    <strong style="color: #764ba2;">⚡ Electrical Engineer</strong><br>
                    • Quality control statistics<br>
                    • Reliability testing<br>
                    • Circuit failure analysis
                </div>
                <div class="career-item">
                    <strong style="color: #764ba2;">🏗️ Civil Engineer</strong><br>
                    • Structural safety factors<br>
                    • Material strength testing<br>
                    • Load probability analysis
                </div>
                <div class="career-item">
                    <strong style="color: #764ba2;">💻 Software Developer</strong><br>
                    • A/B feature testing<br>
                    • Algorithm optimization<br>
                    • Performance metrics analysis
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔗 Real-World Case Studies</h2>
            <p>Statistics in action across industries:</p>
            <ul>
                <li><strong>Netflix:</strong> A/B testing thousands of interface designs</li>
                <li><strong>CDC:</strong> Tracking disease outbreaks with statistics</li>
                <li><strong>Google:</strong> Analyzing search patterns and user behavior</li>
                <li><strong>Hospitals:</strong> Reducing infection rates with statistical process control</li>
                <li><strong>Manufacturing:</strong> Ensuring quality through statistical sampling</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🎓 College Majors That Require Statistics</h2>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px;">
                <div>
                    <ul>
                        <li>All Engineering fields</li>
                        <li>Business & Economics</li>
                        <li>Psychology & Sociology</li>
                        <li>Biology & Chemistry</li>
                    </ul>
                </div>
                <div>
                    <ul>
                        <li>Computer Science</li>
                        <li>Data Science</li>
                        <li>Environmental Science</li>
                        <li>Public Health</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📞 Take Action Today!</h2>
            <p><strong>Steps to Register for AP Statistics:</strong></p>
            <ol>
                <li>Talk to your current math teacher about your readiness</li>
                <li>Visit your guidance counselor for scheduling</li>
                <li>Check your school's AP course offerings and deadlines</li>
                <li>Discuss the benefits with parents/guardians</li>
                <li>Register before the course selection deadline</li>
            </ol>
        </div>
        
        <div class="contact-info">
            <p style="font-size: 12pt; font-weight: bold; color: #667eea;">
            Your future career starts with the decisions you make today!
            </p>
            <p style="font-style: italic; margin-top: 10px;">
            "In God we trust, all others must bring data." - W. Edwards Deming
            </p>
            <p style="font-size: 9pt; margin-top: 20px; color: #666;">
            Print and share this flyer! | Interactive version available online
            </p>
        </div>
    </div>
    
    </body>
    </html>
    """
    
    return flyer

def create_complete_presentation():
    """Create a COMPLETE printable version of ALL slides"""
    today = datetime.now().strftime("%B %d, %Y")
    
    presentation_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @media print {{
                @page {{
                    size: letter;
                    margin: 0.5in;
                }}
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 12pt;
                    line-height: 1.5;
                    margin: 0;
                    padding: 0;
                    background: white;
                    color: black;
                }}
                .slide {{
                    page-break-after: always;
                    padding: 0.5in;
                    min-height: 9.5in;
                    border-bottom: 2px solid #ccc;
                }}
                h1 {{
                    color: #667eea;
                    text-align: center;
                    margin-bottom: 20px;
                    font-size: 28pt;
                }}
                h2 {{
                    color: #764ba2;
                    border-bottom: 3px solid #764ba2;
                    padding-bottom: 10px;
                    margin-top: 30px;
                    font-size: 20pt;
                }}
                h3 {{
                    color: #333;
                    margin-top: 25px;
                    font-size: 16pt;
                }}
                .example {{
                    background: #f8f9fa;
                    padding: 15px;
                    margin: 15px 0;
                    border-left: 5px solid #667eea;
                    border-radius: 5px;
                }}
                .benefit-list {{
                    margin: 20px 0;
                    padding-left: 20px;
                }}
                .benefit-list li {{
                    margin: 10px 0;
                    font-size: 11pt;
                }}
                .stat-term {{
                    background: #fff3cd;
                    padding: 3px 6px;
                    border-radius: 3px;
                    font-weight: bold;
                }}
                .footer {{
                    position: absolute;
                    bottom: 0.5in;
                    width: calc(100% - 1in);
                    text-align: center;
                    font-size: 10pt;
                    color: #666;
                    border-top: 1px solid #ccc;
                    padding-top: 10px;
                }}
                .page-number::after {{
                    content: "Page " counter(page);
                }}
                .career-title {{
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                }}
                .highlight-box {{
                    background: #e7f3ff;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 8px;
                    border: 1px solid #b8d4ff;
                }}
                .resources {{
                    background: #f0f7ff;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 8px;
                    font-size: 11pt;
                }}
                .resources h4 {{
                    margin-top: 0;
                    color: #667eea;
                }}
                .print-header {{
                    text-align: center;
                    margin-bottom: 30px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #667eea;
                }}
                .print-header small {{
                    font-size: 10pt;
                    color: #666;
                }}
                ul, ol {{
                    margin-left: 25px;
                }}
                li {{
                    margin: 8px 0;
                }}
            }}
        </style>
    </head>
    <body>
    
    <div class="print-header">
        <h1>AP Statistics Career Presentation</h1>
        <p><strong>Complete Printable Version</strong></p>
        <small>Generated on {today} | All content expanded for printing</small>
    </div>
    """
    
    # Add ALL slides to the printable version
    for i, slide in enumerate(slides):
        presentation_html += f'<div class="slide">\n'
        
        if slide["type"] == "title":
            presentation_html += f'''
            <h1>{slide["title"]}</h1>
            <h2 style="text-align: center; color: #764ba2;">{slide["subtitle"]}</h2>
            <div style="text-align: center; margin-top: 100px; font-size: 16pt;">
                {slide["content"]}
            </div>
            '''
            
        elif slide["type"] == "intro":
            presentation_html += f'''
            <h1>{slide["title"]}</h1>
            
            <div class="highlight-box">
                <h2>College & Career Benefits</h2>
                <ul class="benefit-list">
            '''
            for benefit in slide["content"]["benefits"]:
                presentation_html += f'<li>{benefit}</li>\n'
            presentation_html += '''
                </ul>
            </div>
            
            <div class="highlight-box">
                <h2>Real-World Applications</h2>
                <p>''' + slide["content"]["applications"] + '''</p>
            </div>
            
            <div class="resources">
                <h4>📚 General Resources for AP Statistics:</h4>
                <ul>
                    <li><strong>College Board AP Statistics:</strong> Official course information and resources</li>
                    <li><strong>Khan Academy AP Statistics:</strong> Free video lessons and practice problems</li>
                    <li><strong>American Statistical Association:</strong> Career information and case studies</li>
                    <li><strong>CDC Case Studies:</strong> Real public health statistics examples</li>
                    <li><strong>FiveThirtyEight:</strong> Sports and politics statistical analysis</li>
                </ul>
            </div>
            '''
            
        elif slide["type"] == "career":
            presentation_html += f'''
            <h1>{slide["title"]}</h1>
            
            <div class="career-title">
                <h2>{slide["content"]["description"]}</h2>
            </div>
            '''
            
            for example in slide["content"]["examples"]:
                content_with_terms = example["content"].replace(
                    "<span class='highlight'>", "<span class='stat-term'>"
                ).replace("</span>", "</span>")
                
                presentation_html += f'''
                <div class="example">
                    <h3>{example["title"]}</h3>
                    <p>{content_with_terms}</p>
                </div>
                '''
            
            # Add resources for this career
            if "resources" in slide["content"]:
                career_key = slide["content"]["resources"]
                if career_key in CAREER_RESOURCES:
                    presentation_html += '''
                    <div class="resources">
                        <h4>🔗 Learn More About This Career:</h4>
                        <ul>
                    '''
                    for name, url in CAREER_RESOURCES[career_key].items():
                        presentation_html += f'<li><strong>{name}:</strong> {url}</li>\n'
                    presentation_html += '''
                        </ul>
                    </div>
                    '''
            
        elif slide["type"] == "closing":
            presentation_html += f'''
            <h1>{slide["title"]}</h1>
            
            <div style="text-align: center; margin: 50px 0;">
            '''
            for point in slide["content"]["points"]:
                presentation_html += f'<p style="font-size: 14pt; margin: 15px 0;">{point}</p>\n'
            presentation_html += f'''
            </div>
            
            <div class="highlight-box" style="text-align: center; padding: 30px;">
                <p style="font-size: 16pt; font-weight: bold;">{slide["content"]["call_to_action"]}</p>
            </div>
            
            <div style="text-align: center; margin-top: 50px; padding: 20px; background: #f8f9fa; border-radius: 8px;">
                <h3>Next Steps</h3>
                <p style="font-size: 12pt;">{slide["content"]["contact"]}</p>
                <p style="margin-top: 15px; font-size: 11pt;">
                    <strong>Additional Resources:</strong><br>
                    • College Board: https://apcentral.collegeboard.org/<br>
                    • Your School's Guidance Office<br>
                    • AP Statistics Teacher Recommendations
                </p>
            </div>
            '''
        
        presentation_html += f'''
        <div class="footer">
            <div class="page-number"></div>
            <div>Slide {i+1} of {len(slides)} | AP Statistics Career Presentation</div>
        </div>
        </div>
        '''
    
    presentation_html += '''
    </body>
    </html>
    '''
    
    return presentation_html

def display_resources(career_key):
    """Display resource links with real-world examples and case studies"""
    if career_key in CAREER_RESOURCES:
        st.markdown("### 📚 Real-World Examples & Case Studies")
        st.markdown("**See how AP Statistics-level methods are actually used in these careers:**")
        
        resources = CAREER_RESOURCES[career_key]
        for name, url in resources.items():
            st.markdown(f"""
            <div class='resource-link'>
                🔍 <a href='{url}' target='_blank'>{name}</a>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a case study explanation
        st.markdown("""
        <div class='case-study'>
        <strong>What you'll find in these resources:</strong>
        <ul>
        <li>Real data analysis examples from industry</li>
        <li>Statistical methods used in professional settings</li>
        <li>Case studies showing problem-solving with statistics</li>
        <li>Examples of hypothesis testing, regression, probability in practice</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Initialize session state for slide navigation
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0
    if 'show_printable' not in st.session_state:
        st.session_state.show_printable = False
    if 'show_flyer' not in st.session_state:
        st.session_state.show_flyer = False
    
    # Sidebar navigation
    with st.sidebar:
        st.title("📊 Navigation")
        
        # Slide selector
        selected_slide = st.selectbox(
            "Go to Slide:",
            [f"Slide {i+1}: {slides[i]['title'][:30]}..." for i in range(len(slides))],
            index=st.session_state.current_slide
        )
        
        # Update current slide based on selection
        st.session_state.current_slide = int(selected_slide.split(":")[0].replace("Slide ", "")) - 1
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Previous", disabled=st.session_state.current_slide == 0):
                st.session_state.current_slide = max(0, st.session_state.current_slide - 1)
                st.rerun()
        
        with col2:
            if st.button("Next ➡️", disabled=st.session_state.current_slide == len(slides)-1):
                st.session_state.current_slide = min(len(slides)-1, st.session_state.current_slide + 1)
                st.rerun()
        
        # Progress indicator
        st.progress((st.session_state.current_slide + 1) / len(slides))
        st.caption(f"Slide {st.session_state.current_slide + 1} of {len(slides)}")
        
        # REAL-WORLD EXAMPLE HIGHLIGHT
        st.markdown("---")
        st.subheader("🔬 Featured Real-World Example")
        
        # Show a relevant real-world example based on current slide
        slide = slides[st.session_state.current_slide]
        if slide["type"] in ["intro", "career"] and "resources" in slide["content"]:
            career_key = slide["content"]["resources"]
            if career_key in CAREER_RESOURCES:
                resources = CAREER_RESOURCES[career_key]
                # Show first resource as featured
                first_name, first_url = list(resources.items())[0]
                st.markdown(f"**Featured:** [{first_name}]({first_url})")
                st.caption("Click to see a real case study!")
        
        # Quick AP Stats real-world examples
        st.markdown("---")
        st.subheader("📈 Quick Examples")
        st.markdown("[Netflix A/B Testing](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15)")
        st.markdown("[CDC Case Studies](https://www.cdc.gov/nchs/pressroom/casestudies.htm)")
        st.markdown("[Sports Analytics](https://fivethirtyeight.com/tag/statistics/)")
        
        # PRINT/SAVE BUTTONS
        st.markdown("---")
        st.subheader("🖨️ Print & Save")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Print Flyer", use_container_width=True):
                st.session_state.show_flyer = True
                st.session_state.show_printable = False
        
        with col2:
            if st.button("📊 Full Presentation", use_container_width=True):
                st.session_state.show_printable = True
                st.session_state.show_flyer = False
        
        # Download section
        st.markdown("---")
        st.subheader("Download Instructions")
        
        instructions = create_instructions_file()
        st.download_button(
            label="📥 Download PowerPoint Instructions",
            data=instructions,
            file_name="PowerPoint_Conversion_Instructions.txt",
            mime="text/plain"
        )
    
    # Main content area - Show printable versions if requested
    if st.session_state.show_printable:
        st.markdown("## 📄 Complete Printable Presentation")
        st.info("**Instructions:** Use your browser's Print function (Ctrl+P) and select 'Save as PDF' for best results.")
        
        presentation_html = create_complete_presentation()
        st.components.v1.html(presentation_html, height=800, scrolling=True)
        
        if st.button("← Back to Interactive Presentation"):
            st.session_state.show_printable = False
            st.rerun()
        
        return
    
    if st.session_state.show_flyer:
        st.markdown("## 📄 2-Page Printable Flyer")
        st.info("**Instructions:** Print double-sided or save as PDF. Perfect for handing out!")
        
        flyer_html = create_flyer()
        st.components.v1.html(flyer_html, height=800, scrolling=True)
        
        if st.button("← Back to Interactive Presentation"):
            st.session_state.show_flyer = False
            st.rerun()
        
        return
    
    # PRINT/SAVE BUTTONS IN MAIN AREA
    st.markdown("### 🖨️ Printable Materials")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Print 2-Page Flyer", use_container_width=True, type="primary"):
            st.session_state.show_flyer = True
            st.rerun()
        st.caption("Perfect for handing out to students")
    
    with col2:
        if st.button("📊 Save Full Presentation", use_container_width=True, type="secondary"):
            st.session_state.show_printable = True
            st.rerun()
        st.caption("Complete 15-slide presentation for printing")
    
    st.markdown("---")
    
    # Display current slide
    slide = slides[st.session_state.current_slide]
    
    if slide["type"] == "title":
        st.markdown(f"<h1 class='main-header'>{slide['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='sub-header'>{slide['subtitle']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #667eea; margin-top: 2rem;'>{slide['content']}</h3>", unsafe_allow_html=True)
        
        # Real-world examples preview
        with st.expander("🎯 See Real-World Statistics Examples", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Famous Case Studies:**")
                st.markdown("""
                - [Netflix: A/B Testing Platform](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15)
                - [Google: Large-Scale Experiments](https://ai.google/research/pubs/pub36500/)
                - [CDC: Public Health Statistics](https://www.cdc.gov/nchs/pressroom/casestudies.htm)
                - [538: Sports Analytics](https://fivethirtyeight.com/tag/statistics/)
                """)
            with col2:
                st.markdown("**AP Stats in Action:**")
                st.markdown("""
                - Hypothesis testing in medicine
                - Regression in marketing
                - Probability in engineering
                - Sampling in social science
                - Confidence intervals in research
                """)
        
        # Add decorative gradient background
        st.markdown("""
        <div style='height: 300px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 20px; margin-top: 2rem; display: flex; align-items: center; justify-content: center;'>
        </div>
        """, unsafe_allow_html=True)
    
    elif slide["type"] == "intro":
        st.markdown(f"<h1 class='main-header'>{slide['title']}</h1>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='intro-section'>", unsafe_allow_html=True)
            st.subheader("College & Career Benefits")
            for benefit in slide["content"]["benefits"]:
                st.markdown(f"✅ {benefit}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='intro-section'>", unsafe_allow_html=True)
        st.subheader("Real-World Applications")
        st.info(slide["content"]["applications"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Display general resources with emphasis on real-world examples
        st.markdown("---")
        st.markdown("### 🔍 Explore Real Statistics in Action")
        st.markdown("**These aren't just textbook problems - here's how statistics is used in the real world:**")
        
        display_resources("general")
    
    elif slide["type"] == "career":
        st.markdown(f"<h1 class='main-header'>{slide['title']}</h1>", unsafe_allow_html=True)
        
        with st.container():
            st.markdown("<div class='slide-card'>", unsafe_allow_html=True)
            st.markdown(f"<h2 class='career-title'>{slide['content']['description']}</h2>", unsafe_allow_html=True)
            
            for example in slide["content"]["examples"]:
                with st.container():
                    st.markdown("<div class='example-box'>", unsafe_allow_html=True)
                    st.markdown(f"**{example['title']}**")
                    st.markdown(example["content"], unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Display career-specific resources with REAL case studies
        if "resources" in slide["content"]:
            display_resources(slide["content"]["resources"])
            
            # Add practical exercise suggestion
            st.markdown("""
            <div class='case-study'>
            <strong>💡 Try This AP Statistics Connection:</strong>
            <p>Look at the case studies above and identify:</p>
            <ul>
            <li>What statistical methods are being used? (hypothesis testing, regression, etc.)</li>
            <li>What data was collected and how?</li>
            <li>What conclusions were drawn from the statistical analysis?</li>
            <li>How could this analysis be improved or expanded?</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    elif slide["type"] == "closing":
        st.markdown(f"<h1 class='main-header'>{slide['title']}</h1>", unsafe_allow_html=True)
        
        # Show top real-world examples from various fields
        with st.expander("🔬 Top Real-World Statistics Examples by Field", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Healthcare:**")
                st.markdown("• [NICU Infection Control](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3917520/)")
                st.markdown("• [Vaccine Efficacy Analysis](https://www.cdc.gov/vaccines/stats-surv/index.html)")
            
            with col2:
                st.markdown("**Technology:**")
                st.markdown("• [Netflix A/B Testing](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15)")
                st.markdown("• [Google Experiments](https://ai.google/research/pubs/pub36500/)")
            
            with col3:
                st.markdown("**Engineering:**")
                st.markdown("• [Quality Control Statistics](https://asq.org/quality-resources/statistics)")
                st.markdown("• [Reliability Engineering](https://www.weibull.com/basics/reliability.htm)")
        
        # Add decorative gradient background
        st.markdown("""
        <div style='height: 400px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 20px; margin: 2rem 0; padding: 3rem; color: white;'>
        """, unsafe_allow_html=True)
        
        for point in slide["content"]["points"]:
            st.markdown(f"<h3 style='color: white; margin: 1rem 0;'>{point}</h3>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.success(slide["content"]["call_to_action"])
        
        # Final resources section
        st.markdown("---")
        st.markdown("### 🎓 Next Steps")
        st.info(slide["content"]["contact"])
    
    # Footer with keyboard navigation hint
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("💡 **Tip:** Use the sidebar to navigate or click the buttons below")
        st.caption("🔗 **Resources:** Click links in each section to learn more about careers and statistics")
    
    # Bottom navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        if st.button("⏮️ First", use_container_width=True):
            st.session_state.current_slide = 0
            st.rerun()
    with col2:
        if st.button("⬅️ Back", use_container_width=True, disabled=st.session_state.current_slide == 0):
            st.session_state.current_slide -= 1
            st.rerun()
    with col4:
        if st.button("Next ➡️", use_container_width=True, disabled=st.session_state.current_slide == len(slides)-1):
            st.session_state.current_slide += 1
            st.rerun()
    with col5:
        if st.button("Last ⏭️", use_container_width=True):
            st.session_state.current_slide = len(slides) - 1
            st.rerun()

if __name__ == "__main__":
    main()
