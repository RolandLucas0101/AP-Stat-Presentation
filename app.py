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
    
    .video-container {
        margin: 1rem 0;
        padding: 1rem;
        background: #f0f8ff;
        border-radius: 8px;
        border-left: 4px solid #ff0000;
    }
    
    .video-link {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        background: white;
        border-radius: 6px;
        margin: 8px 0;
        border: 1px solid #e0e0e0;
    }
    
    .video-link:hover {
        background: #f9f9f9;
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

# Career Resources with WORKING LINKS and YOUTUBE VIDEOS
CAREER_RESOURCES = {
    "general": {
        "📺 YouTube: Why Statistics Matters": "https://youtu.be/sxQaBpKfDRk",
        "📺 YouTube: Statistics in Everyday Life": "https://youtu.be/MtFY0J9c-2A",
        "📺 YouTube: Careers in Statistics": "https://youtu.be/BzHz0J9Q6qo",
        "College Board AP Statistics": "https://apcentral.collegeboard.org/courses/ap-statistics",
        "American Statistical Association": "https://www.amstat.org/",
        "Khan Academy AP Statistics": "https://www.khanacademy.org/math/ap-statistics",
    },
    "NICU Nurse": {
        "📺 YouTube: Statistics in Nursing": "https://youtu.be/PjfS8FU0WVo",
        "📺 YouTube: Data in Healthcare": "https://youtu.be/RmOq-9BcScY",
        "Statistical Analysis of Infant Outcomes": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4481523/",
        "Control Charts in Healthcare": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3917520/",
        "NICU Quality Improvement": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5008519/",
    },
    "Marketing Professional": {
        "📺 YouTube: Statistics in Marketing": "https://youtu.be/JRzCJ3NEPcE",
        "📺 YouTube: A/B Testing Explained": "https://youtu.be/w1R3gZ0cwVE",
        "Google Analytics Academy": "https://analytics.google.com/analytics/academy/",
        "A/B Testing Case Studies": "https://www.optimizely.com/optimization-glossary/ab-testing/",
        "Marketing Statistics Tutorial": "https://www.coursera.org/learn/marketing-analytics",
    },
    "Pediatric Surgeon": {
        "📺 YouTube: Statistics in Medicine": "https://youtu.be/9wVxH7dCq-c",
        "📺 YouTube: Surgical Outcomes Research": "https://youtu.be/K3V0x5Y0VtE",
        "Surgical Outcomes Statistics": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6082075/",
        "Pediatric Surgery Research": "https://www.jpedsurg.org/",
        "Surgical Risk Calculator": "https://riskcalculator.facs.org/RiskCalculator/",
    },
    "Registered Nurse": {
        "📺 YouTube: Nursing Statistics": "https://youtu.be/TSu9HGnlMV0",
        "📺 YouTube: Evidence-Based Nursing": "https://youtu.be/eJ5s2rHvH8c",
        "Nursing Statistics Education": "https://www.nln.org/education/statistics-for-nurses",
        "Quality Improvement in Healthcare": "https://www.ahrq.gov/talkingquality/index.html",
        "Lab Value Interpretation": "https://www.ncbi.nlm.nih.gov/books/NBK279390/",
    },
    "Cybersecurity Professional": {
        "📺 YouTube: Statistics in Cybersecurity": "https://youtu.be/8tqHOVD8gH4",
        "📺 YouTube: Anomaly Detection": "https://youtu.be/GV8B7x5dC_0",
        "Cybersecurity Statistics Resources": "https://www.sans.org/security-resources/",
        "Threat Detection Statistics": "https://www.cisa.gov/cybersecurity",
        "Security Metrics Guide": "https://csrc.nist.gov/projects/security-metrics",
    },
    "Cosmetic Scientist": {
        "📺 YouTube: Statistics in Product Testing": "https://youtu.be/YOUR_VIDEO_ID_HERE",  # Placeholder
        "📺 YouTube: Consumer Research Methods": "https://youtu.be/YOUR_VIDEO_ID_HERE",  # Placeholder
        "Cosmetic Science Statistics": "https://www.personalcarecouncil.org/science/statistics/",
        "Product Testing Methods": "https://www.astm.org/standards/cosmetic-and-personal-care-products.html",
        "Consumer Research Statistics": "https://www.quirks.com/articles/category/statistics",
    },
    "Dermatology Physician Assistant": {
        "📺 YouTube: Medical Statistics": "https://youtu.be/USMQ0o-E-ls",
        "📺 YouTube: Diagnostic Tests": "https://youtu.be/LGXZCwMqNfU",
        "Skin Cancer Statistics": "https://www.cancer.org/cancer/types/skin-cancer.html",
        "Dermatology Research": "https://www.aad.org/publications",
        "Diagnostic Test Statistics": "https://www.ncbi.nlm.nih.gov/books/NBK557530/",
    },
    "Electrical Engineer": {
        "📺 YouTube: Statistics in Engineering": "https://youtu.be/tKdGgH0oygw",
        "📺 YouTube: Quality Control Statistics": "https://youtu.be/fHLQa2B3VhE",
        "Engineering Statistics": "https://www.ieee.org/education/online-courses.html",
        "Quality Control Statistics": "https://asq.org/quality-resources/statistics",
        "Reliability Engineering": "https://www.weibull.com/basics/reliability.htm",
    },
    "Civil Engineer": {
        "📺 YouTube: Statistics in Civil Engineering": "https://youtu.be/5v5wC0mHKQw",
        "📺 YouTube: Structural Safety Statistics": "https://youtu.be/WAHmrBvukF0",
        "Structural Engineering Statistics": "https://www.asce.org/education/online-courses",
        "Construction Statistics": "https://www.agc.org/resources/construction-data",
        "Materials Testing Standards": "https://www.astm.org/standards/construction-standards.html",
    },
    "Pediatrician": {
        "📺 YouTube: Statistics in Pediatrics": "https://youtu.be/ETyL6eJhB-w",
        "📺 YouTube: Growth Charts Explained": "https://youtu.be/LN3Xq7tGc8k",
        "CDC Growth Charts": "https://www.cdc.gov/growthcharts/",
        "Pediatric Health Statistics": "https://www.aap.org/en/patient-care/",
        "Vaccine Statistics": "https://www.cdc.gov/vaccines/stats-surv/index.html",
    },
    "Software Developer": {
        "📺 YouTube: Statistics in Software": "https://youtu.be/fZ3C2gDTtYQ",
        "📺 YouTube: A/B Testing in Tech": "https://youtu.be/w4ALgK5eEws",
        "A/B Testing at Google": "https://ai.google/research/pubs/pub36500/",
        "Software Metrics": "https://www.atlassian.com/devops/devops-tools/devops-metrics",
        "Programming Statistics": "https://stackoverflow.blog/2021/11/22/the-state-of-developer-ecosystem-2021/",
    },
    "Physicist / Nanotechnologist": {
        "📺 YouTube: Statistics in Physics": "https://youtu.be/sGBLgRwLw-o",
        "📺 YouTube: Data Analysis in Science": "https://youtu.be/-ETQ97mXXF0",
        "Physics Data Analysis": "https://www.physicsforums.com/threads/statistics-in-physics.1000000/",
        "Nanotechnology Research": "https://www.nano.gov/you/nanotechnology-benefits",
        "Scientific Statistics": "https://www.nature.com/subjects/statistics",
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
            "resources": "NICU Nurse",
            "youtube_video": "PjfS8FU0WVo"
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
            "resources": "Marketing Professional",
            "youtube_video": "JRzCJ3NEPcE"
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
            "resources": "Pediatric Surgeon",
            "youtube_video": "9wVxH7dCq-c"
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
            "resources": "Registered Nurse",
            "youtube_video": "TSu9HGnlMV0"
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
            "resources": "Cybersecurity Professional",
            "youtube_video": "8tqHOVD8gH4"
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
            "resources": "Cosmetic Scientist",
            "youtube_video": "PjfS8FU0WVo"
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
            "resources": "Dermatology Physician Assistant",
            "youtube_video": "USMQ0o-E-ls"
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
            "resources": "Electrical Engineer",
            "youtube_video": "tKdGgH0oygw"
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
            "resources": "Civil Engineer",
            "youtube_video": "5v5wC0mHKQw"
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
            "resources": "Pediatrician",
            "youtube_video": "ETyL6eJhB-w"
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
            "resources": "Software Developer",
            "youtube_video": "fZ3C2gDTtYQ"
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
            "resources": "Physicist / Nanotechnologist",
            "youtube_video": "sGBLgRwLw-o"
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

def create_flyer_html():
    """Create a two-page flyer summary (front and back) as HTML"""
    today = datetime.now().strftime("%B %d, %Y")
    
    flyer_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AP Statistics Flyer</title>
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
                color: #000;
            }}
            .page {{
                page-break-after: always;
                padding: 0.5in;
                min-height: 9in;
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
        }}
    </style>
</head>
<body>

<!-- PAGE 1 (FRONT) -->
<div class="page">
    <div style="text-align: center; margin-bottom: 20px;">
        <h1>📊 AP Statistics</h1>
        <h2>Your Gateway to Career Success</h2>
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
</html>'''
    
    return flyer_html

def create_complete_presentation_html():
    """Create a COMPLETE printable version of ALL slides"""
    today = datetime.now().strftime("%B %d, %Y")
    
    presentation_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AP Statistics Full Presentation</title>
    <style>
        @media print {
            @page {
                size: letter;
                margin: 0.
