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
</style>
""", unsafe_allow_html=True)

# Updated Career Resources with REAL-WORLD EXAMPLES and CASE STUDIES
CAREER_RESOURCES = {
    "general": {
        "Case Study: How Netflix Uses Statistics": "https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15",
        "Real-World Statistics in Sports Analytics": "https://fivethirtyeight.com/features/how-our-2020-nfl-predictions-work/",
        "Statistics in Public Policy Decision-Making": "https://www.cdc.gov/nchs/pressroom/casestudies.htm",
        "AP Statistics Real-World Applications": "https://apcentral.collegeboard.org/courses/ap-statistics/classroom-resources/real-world-applications",
        "Statistics in Everyday Life - Case Studies": "https://www.amstat.org/asa/files/pdfs/edu-case-studies.pdf",
    },
    "NICU Nurse": {
        "Case Study: Statistical Analysis of Premature Infant Outcomes": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4481523/",
        "Real Example: Using Control Charts in NICU Infection Prevention": "https://www.jstor.org/stable/10.1086/664772",
        "Statistical Methods for Neonatal Risk Assessment": "https://www.sciencedirect.com/science/article/pii/S002234761730555X",
        "AP Stats-Level Study: Temperature Monitoring in Preterm Infants": "https://pubmed.ncbi.nlm.nih.gov/29279822/",
    },
    "Marketing Professional": {
        "Case Study: A/B Testing at Booking.com (10,000+ tests)": "https://booking.ai/ab-testing-at-booking-com-8c6b7a420a79",
        "Real Example: Regression Analysis for Ad Spend Optimization": "https://hbr.org/2014/10/a-refresher-on-regression-analysis",
        "Statistics in Digital Marketing - Facebook Case Study": "https://www.facebook.com/business/success/",
        "AP Stats Application: Customer Segmentation Analysis": "https://towardsdatascience.com/customer-segmentation-using-k-means-clustering-d33964f238c3",
    },
    "Pediatric Surgeon": {
        "Case Study: Statistical Analysis of Appendectomy Outcomes": "https://jamanetwork.com/journals/jamasurgery/fullarticle/2760744",
        "Real Example: Survival Analysis in Pediatric Cancer Surgery": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6082075/",
        "Probability in Surgical Risk Calculators": "https://riskcalculator.facs.org/RiskCalculator/",
        "AP Stats-Level Study: Complication Rates by Surgical Technique": "https://journals.lww.com/annalsofsurgery/Abstract/2019/03000/Use_of_Statistical_Process_Control_in_Surgical.21.aspx",
    },
    "Registered Nurse": {
        "Case Study: Statistical Process Control for Hospital-Acquired Infections": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3917520/",
        "Real Example: Interpreting Lab Values Using Normal Distribution": "https://www.ncbi.nlm.nih.gov/books/NBK279390/",
        "Statistics in Nursing Quality Improvement Projects": "https://www.ahrq.gov/patient-safety/resources/advances-in-patient-safety/vol4/kennedy.html",
        "AP Stats Application: Fall Risk Assessment Scoring": "https://pubmed.ncbi.nlm.nih.gov/29166326/",
    },
    "Cybersecurity Professional": {
        "Case Study: Anomaly Detection Using Statistical Methods at AWS": "https://aws.amazon.com/blogs/security/use-machine-learning-to-detect-anomalies-in-aws-cloudtrail-logs/",
        "Real Example: Bayesian Networks for Threat Detection": "https://www.sciencedirect.com/science/article/pii/S0167404817301577",
        "Statistics in Cybersecurity Incident Response": "https://www.sans.org/white-papers/37155/",
        "AP Stats Application: Network Traffic Pattern Analysis": "https://dl.acm.org/doi/10.1145/3134600.3134646",
    },
    "Cosmetic Scientist": {
        "Case Study: Statistical Design of Experiments for Skincare Products": "https://www.sciencedirect.com/science/article/pii/S101113441830319X",
        "Real Example: Regression Analysis for Cosmetic Formulation": "https://www.cosmeticsandtoiletries.com/testing/statistics/Statistical-Design-of-Experiments-for-Cosmetic-Formulation-570047371.html",
        "Statistics in Consumer Product Testing": "https://www.mdpi.com/2079-9284/8/3/75",
        "AP Stats Application: Shelf-Life Prediction Models": "https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-3010.2006.00573.x",
    },
    "Dermatology Physician Assistant": {
        "Case Study: Diagnostic Accuracy Statistics for Skin Cancer Detection": "https://jamanetwork.com/journals/jamadermatology/fullarticle/2768620",
        "Real Example: Confidence Intervals in Treatment Efficacy Studies": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6899265/",
        "Statistics in Dermatology Clinical Trials": "https://www.jidonline.org/article/S0022-202X(15)41199-5/fulltext",
        "AP Stats Application: ROC Curves for Diagnostic Tests": "https://www.ncbi.nlm.nih.gov/books/NBK557530/",
    },
    "Electrical Engineer": {
        "Case Study: Statistical Quality Control in Semiconductor Manufacturing": "https://www.sciencedirect.com/science/article/pii/S0166361506002305",
        "Real Example: Reliability Engineering Using Weibull Distribution": "https://www.weibull.com/hotwire/issue14/relbasics14.htm",
        "Statistics in Circuit Design and Testing": "https://ieeexplore.ieee.org/document/6682919",
        "AP Stats Application: Tolerance Analysis in Electronic Components": "https://www.allaboutcircuits.com/technical-articles/understanding-statistical-tolerancing-monte-carlo-simulation/",
    },
    "Civil Engineer": {
        "Case Study: Statistical Analysis of Bridge Load Testing": "https://ascelibrary.org/doi/10.1061/%28ASCE%29CF.1943-5509.0001333",
        "Real Example: Probability-Based Structural Safety Factors": "https://www.sciencedirect.com/science/article/pii/S014102961730086X",
        "Statistics in Earthquake Engineering Design": "https://peer.berkeley.edu/publications/peer_reports/reports_2015/web_PEER-2015-05-Moehle.pdf",
        "AP Stats Application: Concrete Strength Sampling and Testing": "https://www.concrete.org/publications/internationalconcreteabstractsportal/m/details/id/51686890",
    },
    "Pediatrician": {
        "Case Study: Growth Chart Percentile Analysis in Clinical Practice": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6410476/",
        "Real Example: Vaccine Efficacy Statistical Analysis": "https://www.nejm.org/doi/full/10.1056/NEJMoa2034577",
        "Statistics in Pediatric Clinical Guidelines": "https://publications.aap.org/pediatrics/article/145/3/e20193997/76925/Clinical-Practice-Guideline-for-the-Evaluation-and",
        "AP Stats Application: Developmental Screening Test Statistics": "https://www.cdc.gov/ncbddd/actearly/pdf/help_pdfs/cdc_developmental_screening_guide_508.pdf",
    },
    "Software Developer": {
        "Case Study: A/B Testing Statistics at Google (Large-Scale)": "https://ai.google/research/pubs/pub36500/",
        "Real Example: Statistical Methods in Netflix Recommendation Algorithm": "https://netflixtechblog.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429",
        "Statistics in Software Performance Testing": "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2001-87.pdf",
        "AP Stats Application: Error Rate Analysis in Code Deployment": "https://engineering.fb.com/2015/08/06/production-engineering/safe-and-fast-deploys-at-facebook/",
    },
    "Physicist / Nanotechnologist": {
        "Case Study: Statistical Analysis in Large Hadron Collider Experiments": "https://cds.cern.ch/record/2017902/files/CERN-Brochure-2014-002-Eng.pdf",
        "Real Example: Uncertainty Analysis in Nanoscale Measurements": "https://www.nature.com/articles/s41565-020-0658-9",
        "Statistics in Materials Science Research": "https://www.sciencedirect.com/science/article/pii/S1359645419305711",
        "AP Stats Application: Particle Distribution Analysis": "https://iopscience.iop.org/article/10.1088/1361-6463/ab5b8c",
    }
}

# App data (same structure, but with resource keys)
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
                }}
                .page {{
                    page-break-after: always;
                    padding: 20px;
                }}
                .page-break {{
                    page-break-before: always;
                }}
                h1 {{
                    color: #667eea;
                    text-align: center;
                    margin-bottom: 10px;
                }}
                h2 {{
                    color: #764ba2;
                    border-bottom: 2px solid #764ba2;
                    padding-bottom: 5px;
                }}
                .highlight {{
                    background-color: #fff3cd;
                    padding: 2px 4px;
                    border-radius: 3px;
                }}
                .section {{
                    margin: 15px 0;
                    padding: 10px;
                    background: #f8f9fa;
                    border-radius: 5px;
                }}
                .career-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 10px;
                    margin: 15px 0;
                }}
                .career-item {{
                    padding: 8px;
                    background: white;
                    border: 1px solid #dee2e6;
                    border-radius: 4px;
                }}
                .stat-method {{
                    background: #e7f3ff;
                    padding: 5px;
                    margin: 3px 0;
                    border-left: 3px solid #667eea;
                }}
                .contact-info {{
                    text-align: center;
                    margin-top: 20px;
                    font-size: 10pt;
                }}
            }}
        </style>
    </head>
    <body>
    
    <!-- PAGE 1 (FRONT) -->
    <div class="page">
        <h1>📊 AP Statistics: Your Gateway to Career Success</h1>
        <p style="text-align: center; font-weight: bold;">Why Juniors Should Take AP Stats Senior Year</p>
        <p style="text-align: center; font-size: 10pt;">{today}</p>
        
        <div class="section">
            <h2>🚀 Key Benefits of AP Statistics</h2>
            <ul>
                <li><strong>College Credit:</strong> Earn credits and save tuition money</li>
                <li><strong>College Admissions:</strong> Stand out in competitive applications</li>
                <li><strong>Career Preparation:</strong> Required for most STEM and business majors</li>
                <li><strong>Real-World Skills:</strong> Data analysis, critical thinking, problem-solving</li>
                <li><strong>Versatility:</strong> Applies to ANY career field</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🎯 AP Statistics in Real Careers</h2>
            <div class="career-grid">
                <div class="career-item">
                    <strong>🏥 NICU Nurse</strong><br>
                    • Vital sign analysis<br>
                    • Treatment effectiveness testing<br>
                    • Infection control statistics
                </div>
                <div class="career-item">
                    <strong>📈 Marketing Pro</strong><br>
                    • A/B testing campaigns<br>
                    • Customer segmentation<br>
                    • ROI analysis
                </div>
                <div class="career-item">
                    <strong>⚕️ Pediatric Surgeon</strong><br>
                    • Surgical risk assessment<br>
                    • Outcome prediction<br>
                    • Clinical trial analysis
                </div>
                <div class="career-item">
                    <strong>🔒 Cybersecurity</strong><br>
                    • Anomaly detection<br>
                    • Threat probability<br>
                    • Risk modeling
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>📚 AP Stats Methods You'll Learn</h2>
            <div class="stat-method">Hypothesis Testing</div>
            <div class="stat-method">Regression Analysis</div>
            <div class="stat-method">Probability Distributions</div>
            <div class="stat-method">Confidence Intervals</div>
            <div class="stat-method">Sampling Methods</div>
            <div class="stat-method">Experimental Design</div>
        </div>
        
        <div class="contact-info">
            <p><strong>Questions?</strong> Talk to your guidance counselor about registering for AP Statistics!</p>
            <p>Visit: [Your School's AP Coordinator] | Email: [Contact Information]</p>
        </div>
    </div>
    
    <!-- PAGE 2 (BACK) -->
    <div class="page page-break">
        <h1>AP Statistics Career Connections</h1>
        
        <div class="section">
            <h2>💡 More Career Examples</h2>
            <div class="career-grid">
                <div class="career-item">
                    <strong>🧪 Cosmetic Scientist</strong><br>
                    • Product testing stats<br>
                    • Formulation optimization<br>
                    • Consumer research
                </div>
                <div class="career-item">
                    <strong>⚡ Electrical Engineer</strong><br>
                    • Quality control<br>
                    • Reliability testing<br>
                    • Circuit analysis
                </div>
                <div class="career-item">
                    <strong>🏗️ Civil Engineer</strong><br>
                    • Structural safety<br>
                    • Material testing<br>
                    • Load analysis
                </div>
                <div class="career-item">
                    <strong>💻 Software Developer</strong><br>
                    • A/B feature testing<br>
                    • Algorithm optimization<br>
                    • Performance metrics
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔗 Real-World Case Studies</h2>
            <p>See how statistics is used in industry:</p>
            <ul>
                <li><strong>Netflix:</strong> A/B testing platform with thousands of experiments</li>
                <li><strong>CDC:</strong> Public health statistics and disease tracking</li>
                <li><strong>Google:</strong> Large-scale experimentation and analysis</li>
                <li><strong>Hospitals:</strong> Quality improvement and patient safety stats</li>
                <li><strong>Manufacturing:</strong> Statistical process control and quality</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>🎓 College Majors That Require Statistics</h2>
            <ul>
                <li>All Engineering disciplines</li>
                <li>Business & Economics</li>
                <li>Psychology & Social Sciences</li>
                <li>Biology & Health Sciences</li>
                <li>Computer Science & Data Science</li>
                <li>Environmental Science</li>
                <li>Education Research</li>
            </ul>
        </div>
        
        <div class="section">
            <h2>📞 Take Action Today!</h2>
            <p><strong>Steps to Register:</strong></p>
            <ol>
                <li>Talk to your current math teacher</li>
                <li>Visit your guidance counselor</li>
                <li>Check your school's AP course offerings</li>
                <li>Discuss with parents/guardians</li>
                <li>Register before the deadline</li>
            </ol>
        </div>
        
        <div class="contact-info">
            <p><strong>Remember:</strong> Your future career starts with the decisions you make today!</p>
            <p>"In God we trust, all others must bring data." - W. Edwards Deming</p>
            <p style="font-size: 9pt; margin-top: 20px;">Print this flyer and share with friends!</p>
        </div>
    </div>
    
    </body>
    </html>
    """
    
    return flyer

def create_presentation_pdf():
    """Create a PDF version of the entire presentation"""
    today = datetime.now().strftime("%B %d, %Y")
    
    pdf_content = f"""
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
                }}
                .slide {{
                    page-break-after: always;
                    padding: 20px;
                    border: 1px solid #ccc;
                    margin-bottom: 20px;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    min-height: 9in;
                }}
                h1 {{
                    color: #667eea;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                h2 {{
                    color: #764ba2;
                    border-bottom: 3px solid #764ba2;
                    padding-bottom: 10px;
                }}
                .example {{
                    background: white;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #667eea;
                    border-radius: 5px;
                }}
                .footer {{
                    position: absolute;
                    bottom: 10px;
                    width: 100%;
                    text-align: center;
                    font-size: 10pt;
                    color: #666;
                }}
                .page-number::after {{
                    content: "Page " counter(page);
                }}
            }}
        </style>
    </head>
    <body>
    
    <div class="slide">
        <h1>📊 AP Statistics</h1>
        <h2 style="text-align: center; color: #764ba2;">Your Gateway to Career Success</h2>
        <p style="text-align: center; font-size: 14pt; margin-top: 40px;">Why Juniors Should Take AP Stats Senior Year</p>
        <p style="text-align: center; font-size: 10pt; margin-top: 100px;">Presentation Date: {today}</p>
        <div class="footer">
            <span class="page-number"></span>
        </div>
    </div>
    
    <div class="slide">
        <h1>Why AP Statistics Matters</h1>
        <h2>College & Career Benefits</h2>
        <ul>
            <li>Required or recommended for MOST college majors</li>
            <li>Earn college credit and save tuition money</li>
            <li>Build critical thinking and data analysis skills</li>
            <li>Stand out on college applications</li>
            <li>Prepare for data-driven careers in ANY field</li>
        </ul>
        
        <h2>Real-World Applications</h2>
        <p>Whether you're interested in healthcare, technology, engineering, business, or research, 
        statistics is the foundation of decision-making in the modern workplace.</p>
        
        <div class="footer">
            <span class="page-number"></span>
        </div>
    </div>
    
    <div class="slide">
        <h1>🏥 NICU Nurse</h1>
        <h2>How Statistics Empowers NICU Nurses</h2>
        
        <div class="example">
            <h3>Patient Monitoring & Risk Assessment</h3>
            <p>NICU nurses analyze vital sign patterns (heart rate, oxygen levels, temperature) to detect abnormalities. 
            Using statistical concepts like mean, standard deviation, and outliers, you can identify when a baby's 
            vitals fall outside normal ranges.</p>
        </div>
        
        <div class="example">
            <h3>Treatment Effectiveness Analysis</h3>
            <p>When implementing care protocols, nurses track outcomes across multiple patients. Using hypothesis 
            testing and confidence intervals, you can determine if new treatments significantly improve outcomes.</p>
        </div>
        
        <div class="footer">
            <span class="page-number"></span>
        </div>
    </div>
    
    <!-- Continue with other slides... -->
    
    <div class="slide">
        <h1>Take AP Statistics Next Year!</h1>
        <h2 style="text-align: center; color: #667eea;">Your Future Starts Now</h2>
        
        <div style="text-align: center; margin: 40px 0;">
            <p style="font-size: 14pt; margin: 10px;">✓ Prepare for ANY college major</p>
            <p style="font-size: 14pt; margin: 10px;">✓ Build essential career skills</p>
            <p style="font-size: 14pt; margin: 10px;">✓ Earn college credit</p>
            <p style="font-size: 14pt; margin: 10px;">✓ Stand out to admissions</p>
        </div>
        
        <div style="text-align: center; margin-top: 60px;">
            <p style="font-size: 16pt; font-weight: bold; color: #764ba2;">
            Your future career starts with the decisions you make today! 📊
            </p>
            <p style="margin-top: 30px;">
            Questions? Talk to your guidance counselor about registering for AP Statistics!
            </p>
        </div>
        
        <div class="footer">
            <span class="page-number"></span>
        </div>
    </div>
    
    </body>
    </html>
    """
    
    # Add all career slides
    for slide in slides[2:-1]:  # Skip title and intro slides, and closing slide
        if slide["type"] == "career":
            career_html = f"""
            <div class="slide">
                <h1>{slide['title']}</h1>
                <h2>{slide['content']['description']}</h2>
            """
            
            for example in slide["content"]["examples"]:
                career_html += f"""
                <div class="example">
                    <h3>{example['title']}</h3>
                    <p>{example['content'].replace('<span class=\'highlight\'>', '').replace('</span>', '')}</p>
                </div>
                """
            
            career_html += """
                <div class="footer">
                    <span class="page-number"></span>
                </div>
            </div>
            """
            pdf_content = pdf_content.replace("<!-- Continue with other slides... -->", career_html + "\n<!-- Continue with other slides... -->")
    
    pdf_content = pdf_content.replace("<!-- Continue with other slides... -->", "")
    
    return pdf_content

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
        st.markdown("[Sports Analytics](https://fivethirtyeight.com/features/how-our-2020-nfl-predictions-work/)")
        
        # PRINT/SAVE BUTTONS
        st.markdown("---")
        st.subheader("🖨️ Print & Save")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Print Flyer", use_container_width=True):
                flyer_html = create_flyer()
                st.markdown(f'<iframe src="data:text/html;base64,{base64.b64encode(flyer_html.encode()).decode()}" width="100%" height="500"></iframe>', unsafe_allow_html=True)
                st.info("Use your browser's Print function (Ctrl+P) to print the flyer")
        
        with col2:
            if st.button("📊 Save Presentation", use_container_width=True):
                pdf_html = create_presentation_pdf()
                st.markdown(f'<iframe src="data:text/html;base64,{base64.b64encode(pdf_html.encode()).decode()}" width="100%" height="500"></iframe>', unsafe_allow_html=True)
                st.info("Use your browser's Print function (Ctrl+P) and select 'Save as PDF'")
        
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
    
    # Main content area
    slide = slides[st.session_state.current_slide]
    
    # PRINT/SAVE BUTTONS IN MAIN AREA
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🖨️ Print 2-Page Flyer Summary", use_container_width=True, type="primary"):
            flyer_html = create_flyer()
            st.markdown(f'<iframe src="data:text/html;base64,{base64.b64encode(flyer_html.encode()).decode()}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
            st.success("Flyer loaded! Use Ctrl+P to print or save as PDF.")
    
    with col2:
        if st.button("💾 Save Full Presentation", use_container_width=True, type="secondary"):
            pdf_html = create_presentation_pdf()
            st.markdown(f'<iframe src="data:text/html;base64,{base64.b64encode(pdf_html.encode()).decode()}" width="100%" height="600"></iframe>', unsafe_allow_html=True)
            st.success("Presentation loaded! Use Ctrl+P and select 'Save as PDF'.")
    
    st.markdown("---")
    
    # Display slide based on type
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
                - [538: Sports Analytics](https://fivethirtyeight.com/features/how-our-2020-nfl-predictions-work/)
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
                st.markdown("• [NICU Infection Control](https://www.jstor.org/stable/10.1086/664772)")
                st.markdown("• [Vaccine Efficacy Analysis](https://www.nejm.org/doi/full/10.1056/NEJMoa2034577)")
            
            with col2:
                st.markdown("**Technology:**")
                st.markdown("• [Netflix A/B Testing](https://netflixtechblog.com/its-all-a-bout-testing-the-netflix-experimentation-platform-4e1ca458c15)")
                st.markdown("• [Google Experiments](https://ai.google/research/pubs/pub36500/)")
            
            with col3:
                st.markdown("**Engineering:**")
                st.markdown("• [Bridge Load Testing](https://ascelibrary.org/doi/10.1061/%28ASCE%29CF.1943-5509.0001333)")
                st.markdown("• [Quality Control](https://www.sciencedirect.com/science/article/pii/S0166361506002305)")
        
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
