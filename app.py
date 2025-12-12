import streamlit as st
import base64
from io import BytesIO
from datetime import datetime
import urllib.parse

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
    
    .teacher-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 15px;
        margin: 1rem 0 2rem 0;
        border: 2px solid #fff;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .teacher-banner h2 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
        font-weight: bold;
        line-height: 1.2;
    }
    
    .teacher-banner h3 {
        color: white;
        margin: 1rem 0 0.5rem 0;
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    .teacher-banner p {
        color: #f0f0f0;
        margin: 0.25rem 0;
        font-size: 1.3rem;
        line-height: 1.4;
    }
    
    .teacher-credit {
        margin-top: 1rem;
        font-size: 1.1rem;
        color: #e0e0e0;
        font-style: italic;
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
    
    .schedule-box {
        background: linear-gradient(135deg, #f0f7ff 0%, #e6f2ff 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #667eea;
    }
    
    .schedule-year {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #764ba2;
    }
    
    .search-container {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #28a745;
    }
    
    .search-keyword {
        display: inline-block;
        background: #e7f3ff;
        padding: 6px 12px;
        margin: 4px;
        border-radius: 20px;
        cursor: pointer;
        border: 1px solid #667eea;
        font-size: 0.9rem;
    }
    
    .search-keyword:hover {
        background: #d0e7ff;
    }
    
    .youtube-search-btn {
        background: #ff0000;
        color: white;
        padding: 8px 16px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-weight: bold;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .working-video {
        background: #d4edda;
        border-left: 4px solid #28a745;
    }
    
    .alternative-video {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    
    .clickable-link {
        display: block;
        padding: 10px 15px;
        margin: 5px 0;
        background: #ff0000;
        color: white;
        text-align: center;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
    }
    
    .clickable-link:hover {
        background: #cc0000;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# GUARANTEED WORKING YOUTUBE VIDEOS (TESTED)
GUARANTEED_VIDEOS = {
    "general_stats": {
        "title": "What is Statistics?",
        "url": "https://www.youtube.com/watch?v=LMSyiAJm99g",
        "description": "Khan Academy introduction to statistics"
    },
    "stats_basics": {
        "title": "Introduction to Statistics",
        "url": "https://www.youtube.com/watch?v=GUQJ7zMoSCM",
        "description": "Basic concepts of statistics"
    },
    "stats_careers": {
        "title": "Statistics Careers",
        "url": "https://www.youtube.com/watch?v=kyjlxsLW1Is",
        "description": "Careers in statistics"
    }
}

# YouTube Search Keywords for each career
YOUTUBE_SEARCH_KEYWORDS = {
    "NICU Nurse": [
        "statistics nursing NICU",
        "medical statistics for nurses",
        "data analysis in healthcare",
        "statistics in neonatal care",
        "evidence-based practice nursing"
    ],
    "Marketing Professional": [
        "statistics in marketing",
        "marketing analytics",
        "A/B testing statistics",
        "data-driven marketing",
        "market research statistics"
    ],
    "Pediatric Surgeon": [
        "medical statistics",
        "surgical outcomes statistics",
        "clinical research statistics",
        "statistics in medicine",
        "evidence-based surgery"
    ],
    "Registered Nurse": [
        "nursing statistics",
        "healthcare data analysis",
        "patient care statistics",
        "quality improvement statistics",
        "nursing research statistics"
    ],
    "Cybersecurity Professional": [
        "statistics in cybersecurity",
        "data analysis security",
        "threat detection statistics",
        "security analytics",
        "cybersecurity data science"
    ],
    "Cosmetic Scientist": [
        "statistics in cosmetics",
        "product testing statistics",
        "cosmetic research statistics",
        "quality control statistics",
        "experimental design cosmetics"
    ],
    "Dermatology Physician Assistant": [
        "medical statistics dermatology",
        "skin care statistics",
        "clinical dermatology research",
        "medical data analysis",
        "dermatology research statistics"
    ],
    "Electrical Engineer": [
        "statistics for engineers",
        "engineering statistics",
        "quality control statistics engineering",
        "reliability engineering statistics",
        "electrical engineering data analysis"
    ],
    "Civil Engineer": [
        "statistics civil engineering",
        "structural engineering statistics",
        "construction statistics",
        "engineering data analysis",
        "civil engineering quality control"
    ],
    "Pediatrician": [
        "medical statistics pediatrics",
        "child health statistics",
        "pediatric research statistics",
        "growth chart statistics",
        "pediatric medicine data analysis"
    ],
    "Software Developer": [
        "statistics for software developers",
        "A/B testing software",
        "data analysis programming",
        "software metrics statistics",
        "machine learning statistics"
    ],
    "Physicist / Nanotechnologist": [
        "statistics in physics",
        "scientific data analysis",
        "research statistics",
        "nanotechnology data analysis",
        "physics experiment statistics"
    ],
    "general": [
        "introduction to statistics",
        "AP statistics course",
        "statistics for beginners",
        "real-world statistics",
        "careers in statistics"
    ]
}

# New Jersey College Schedules (unchanged from original)
NJ_COLLEGE_SCHEDULES = {
    "NICU Nurse": {
        "school": "Rutgers University School of Nursing",
        "major": "Bachelor of Science in Nursing (BSN)",
        "schedule": {
            "Year 1": ["General Biology", "General Chemistry", "Anatomy & Physiology I", "College Writing", "Statistics (AP Credit Accepted!)"],
            "Year 2": ["Anatomy & Physiology II", "Microbiology", "Pathophysiology", "Nursing Fundamentals", "Health Assessment"],
            "Year 3": ["Medical-Surgical Nursing", "Pediatric Nursing", "Pharmacology", "Research in Nursing", "Clinical Rotations"],
            "Year 4": ["Maternal-Child Nursing", "Community Health Nursing", "NICU Specialization", "Nursing Leadership", "Capstone Clinical"]
        },
        "stats_note": "Statistics is a REQUIRED course for all nursing majors. AP Statistics credit fulfills this requirement."
    },
    "Marketing Professional": {
        "school": "Rutgers Business School",
        "major": "Bachelor of Science in Marketing",
        "schedule": {
            "Year 1": ["Principles of Marketing", "Microeconomics", "Business Statistics (AP Credit Accepted!)", "Financial Accounting", "Business Ethics"],
            "Year 2": ["Consumer Behavior", "Marketing Research", "Macroeconomics", "Management Information Systems", "Business Law"],
            "Year 3": ["Digital Marketing", "Brand Management", "Marketing Analytics", "Sales Management", "Elective"],
            "Year 4": ["Marketing Strategy", "International Marketing", "Marketing Capstone", "Professional Development", "Internship"]
        },
        "stats_note": "Business Statistics is CORE to marketing analytics. AP Stats gives you a significant advantage."
    },
    "Pediatric Surgeon": {
        "school": "Rutgers Robert Wood Johnson Medical School (Pre-med track)",
        "major": "Biology/Pre-medical Studies",
        "schedule": {
            "Year 1": ["General Biology I & II", "General Chemistry I & II", "Calculus I", "Statistics for Life Sciences (AP Credit Accepted!)"],
            "Year 2": ["Organic Chemistry I & II", "Physics I & II", "Cell Biology", "Genetics", "Biochemistry"],
            "Year 3": ["Human Anatomy", "Physiology", "Microbiology", "Research Methods", "MCAT Preparation"],
            "Year 4": ["Advanced Biology Electives", "Medical Ethics", "Senior Thesis", "Shadowing Experience", "Medical School Applications"]
        },
        "stats_note": "Statistics is ESSENTIAL for medical research and understanding clinical studies."
    },
    "Registered Nurse": {
        "school": "Montclair State University Nursing Program",
        "major": "Bachelor of Science in Nursing",
        "schedule": {
            "Year 1": ["Human Biology", "General Chemistry", "Introduction to Nursing", "Statistics for Health Sciences (AP Credit Accepted!)", "First Year Seminar"],
            "Year 2": ["Anatomy & Physiology", "Microbiology", "Health Assessment", "Pathophysiology", "Clinical Skills Lab"],
            "Year 3": ["Adult Health Nursing", "Mental Health Nursing", "Pharmacology", "Nursing Research", "Clinical Practice"],
            "Year 4": ["Community Health", "Nursing Leadership", "Complex Care Nursing", "Capstone Experience", "NCLEX Preparation"]
        },
        "stats_note": "Statistics is required for evidence-based practice and nursing research courses."
    },
    "Cybersecurity Professional": {
        "school": "New Jersey Institute of Technology (NJIT)",
        "major": "Bachelor of Science in Cybersecurity",
        "schedule": {
            "Year 1": ["Introduction to Cybersecurity", "Programming Fundamentals", "Discrete Mathematics", "Statistics for Computing (AP Credit Accepted!)"],
            "Year 2": ["Network Security", "Cryptography", "Operating Systems", "Data Structures", "Ethical Hacking"],
            "Year 3": ["Digital Forensics", "Security Analytics", "Cloud Security", "Risk Management", "Elective"],
            "Year 4": ["Cyber Defense", "Security Governance", "Capstone Project", "Internship", "Professional Certification Prep"]
        },
        "stats_note": "Statistics is crucial for threat detection algorithms and security analytics."
    },
    "Cosmetic Scientist": {
        "school": "Rutgers School of Pharmacy",
        "major": "Pharmaceutical Sciences/Cosmetic Science",
        "schedule": {
            "Year 1": ["General Chemistry", "Biology", "Calculus", "Statistics for Sciences (AP Credit Accepted!)", "Introduction to Cosmetic Science"],
            "Year 2": ["Organic Chemistry", "Physics", "Biochemistry", "Dermatology Basics", "Product Formulation"],
            "Year 3": ["Analytical Chemistry", "Product Testing Methods", "Regulatory Affairs", "Quality Control", "Research Methods"],
            "Year 4": ["Advanced Formulation", "Stability Testing", "Cosmetic Regulations", "Capstone Project", "Industry Internship"]
        },
        "stats_note": "Statistics is required for product testing, quality control, and research."
    },
    "Dermatology Physician Assistant": {
        "school": "Rutgers Physician Assistant Program (Pre-PA track)",
        "major": "Health Sciences/Pre-Physician Assistant",
        "schedule": {
            "Year 1": ["Human Biology", "General Chemistry", "Medical Terminology", "Statistics for Health Professions (AP Credit Accepted!)"],
            "Year 2": ["Anatomy & Physiology", "Microbiology", "Psychology", "Organic Chemistry", "Pathophysiology"],
            "Year 3": ["Genetics", "Pharmacology", "Medical Ethics", "Research Methods", "Patient Care Experience"],
            "Year 4": ["Advanced Health Assessment", "Clinical Medicine", "Healthcare Systems", "PA School Prerequisites", "Application Preparation"]
        },
        "stats_note": "Statistics is required for PA program admission and understanding clinical research."
    },
    "Electrical Engineer": {
        "school": "New Jersey Institute of Technology (NJIT)",
        "major": "Bachelor of Science in Electrical Engineering",
        "schedule": {
            "Year 1": ["Engineering Fundamentals", "Calculus I & II", "Physics I & II", "Programming for Engineers", "Probability & Statistics (AP Credit Accepted!)"],
            "Year 2": ["Circuit Analysis", "Digital Logic Design", "Signals & Systems", "Electromagnetics", "Engineering Mathematics"],
            "Year 3": ["Electronic Devices", "Control Systems", "Power Systems", "Communication Systems", "Lab Courses"],
            "Year 4": ["Senior Design Project", "Technical Electives", "Power Electronics", "Embedded Systems", "Professional Practice"]
        },
        "stats_note": "Probability & Statistics is a CORE engineering requirement for reliability analysis."
    },
    "Civil Engineer": {
        "school": "Rutgers School of Engineering",
        "major": "Bachelor of Science in Civil Engineering",
        "schedule": {
            "Year 1": ["Engineering Graphics", "Calculus I & II", "Physics I & II", "Chemistry for Engineers", "Engineering Statistics (AP Credit Accepted!)"],
            "Year 2": ["Statics", "Dynamics", "Mechanics of Materials", "Surveying", "Materials Science"],
            "Year 3": ["Structural Analysis", "Geotechnical Engineering", "Transportation Engineering", "Hydraulics", "Environmental Engineering"],
            "Year 4": ["Senior Design Project", "Construction Management", "Structural Design", "Electives", "Professional Development"]
        },
        "stats_note": "Engineering Statistics is required for structural safety analysis and quality control."
    },
    "Pediatrician": {
        "school": "Rutgers University (Pre-med track)",
        "major": "Biology/Pre-medical Studies",
        "schedule": {
            "Year 1": ["General Biology", "General Chemistry", "Calculus", "Statistics for Biology (AP Credit Accepted!)", "Introduction to Medicine"],
            "Year 2": ["Organic Chemistry", "Physics", "Genetics", "Psychology", "Child Development"],
            "Year 3": ["Biochemistry", "Cell Biology", "Physiology", "Research Methods", "MCAT Preparation"],
            "Year 4": ["Immunology", "Neuroscience", "Medical Ethics", "Pediatrics Elective", "Medical School Applications"]
        },
        "stats_note": "Statistics is crucial for interpreting medical research and clinical studies."
    },
    "Software Developer": {
        "school": "Rutgers School of Arts and Sciences",
        "major": "Computer Science",
        "schedule": {
            "Year 1": ["Introduction to Computer Science", "Calculus I", "Discrete Mathematics", "Statistics for CS (AP Credit Accepted!)", "Data Structures"],
            "Year 2": ["Computer Architecture", "Algorithms", "Software Methodology", "Systems Programming", "Linear Algebra"],
            "Year 3": ["Operating Systems", "Database Systems", "Computer Networks", "Elective", "Internship"],
            "Year 4": ["Software Engineering", "Capstone Project", "Advanced Electives", "Professional Development", "Job Preparation"]
        },
        "stats_note": "Statistics is essential for A/B testing, machine learning, and data analysis."
    },
    "Physicist / Nanotechnologist": {
        "school": "Rutgers School of Arts and Sciences",
        "major": "Physics/Nanotechnology",
        "schedule": {
            "Year 1": ["Physics I & II", "Calculus I & II", "General Chemistry", "Statistics for Physical Sciences (AP Credit Accepted!)"],
            "Year 2": ["Modern Physics", "Multivariable Calculus", "Electricity & Magnetism", "Thermal Physics", "Computer Programming"],
            "Year 3": ["Quantum Mechanics", "Solid State Physics", "Nanotechnology Fundamentals", "Research Methods", "Lab Courses"],
            "Year 4": ["Advanced Physics Labs", "Senior Thesis", "Specialized Electives", "Graduate School Prep", "Professional Development"]
        },
        "stats_note": "Statistics is required for experimental data analysis and uncertainty quantification."
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

def create_youtube_search_url(search_query):
    """Create a YouTube search URL"""
    encoded_query = urllib.parse.quote(search_query)
    return f"https://www.youtube.com/results?search_query={encoded_query}"

def display_youtube_search(career_name, keywords=None):
    """Display YouTube search functionality for a career"""
    if not keywords:
        keywords = YOUTUBE_SEARCH_KEYWORDS.get(career_name, [])
    
    st.markdown("### 🔍 Search YouTube for Videos")
    st.markdown(f"**Find current videos about statistics in {career_name}:**")
    
    # Display search keywords as clickable links
    st.markdown("**Suggested search terms (click to open):**")
    
    for idx, keyword in enumerate(keywords[:6]):  # Show up to 6 keywords
        search_url = create_youtube_search_url(keyword)
        st.markdown(f"""
        <a href="{search_url}" target="_blank" class="clickable-link">
        🔍 {keyword}
        </a>
        """, unsafe_allow_html=True)
    
    # Custom search box
    st.markdown("**Or enter your own search:**")
    col1, col2 = st.columns([3, 1])
    with col1:
        custom_search = st.text_input(
            "Search YouTube:",
            value=f"statistics in {career_name}",
            key=f"custom_search_{career_name}",
            placeholder=f"Search for statistics in {career_name}..."
        )
    with col2:
        if custom_search:
            search_url = create_youtube_search_url(custom_search)
            st.markdown(f"""
            <a href="{search_url}" target="_blank" class="clickable-link" style="margin-top: 26px;">
            🔍 Search
            </a>
            """, unsafe_allow_html=True)
    
    # Display guaranteed working videos
    st.markdown("### ✅ Guaranteed Working Videos")
    st.markdown("**These videos are always available (click to watch):**")
    
    for key, video in GUARANTEED_VIDEOS.items():
        st.markdown(f"""
        <div class='resource-link working-video'>
            ▶️ <a href='{video['url']}' target='_blank'>{video['title']}</a>
            <br><small>{video['description']}</small>
        </div>
        """, unsafe_allow_html=True)

def display_career_resources(career_key, career_name):
    """Display resources for a specific career"""
    st.markdown("### 📚 Learning Resources")
    
    # Display guaranteed working videos first
    display_youtube_search(career_name)
    
    # Additional resources section
    st.markdown("### 📖 Additional Learning Materials")
    st.markdown("""
    <div class='case-study'>
    <strong>Where to find more information:</strong>
    <ul>
    <li><strong>Khan Academy AP Statistics:</strong> Free comprehensive course</li>
    <li><strong>College Board AP Statistics:</strong> Official course description and exam info</li>
    <li><strong>Your school library:</strong> Ask for statistics textbooks and career guides</li>
    <li><strong>Professional associations:</strong> Many offer student resources</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

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

OPT
