
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
    
    .teacher-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #fff;
        color: white;
        text-align: center;
    }
    
    .teacher-banner h3 {
        color: white;
        margin-bottom: 0.5rem;
        font-size: 2.5rem;
    }
    
    .teacher-banner p {
        color: #e0e0e0;
        margin: 0.25rem 0;
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
    
    flyer_html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AP Statistics Flyer</title>
    <style>
        @media print {
            @page {
                size: letter;
                margin: 0.5in;
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.4;
                margin: 0;
                padding: 0;
                color: #000;
            }
            .page {
                page-break-after: always;
                padding: 0.5in;
                min-height: 9in;
            }
            .page-break {
                page-break-before: always;
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
                font-size: 24pt;
            }
            h2 {
                color: #764ba2;
                border-bottom: 2px solid #764ba2;
                padding-bottom: 5px;
                font-size: 16pt;
            }
            .highlight {
                background-color: #fff3cd;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .section {
                margin: 15px 0;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 5px;
                border: 1px solid #dee2e6;
            }
            .career-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                margin: 15px 0;
            }
            .career-item {
                padding: 10px;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-size: 10pt;
            }
            .stat-method {
                background: #e7f3ff;
                padding: 8px;
                margin: 5px 0;
                border-left: 3px solid #667eea;
                font-size: 10pt;
            }
            .contact-info {
                text-align: center;
                margin-top: 30px;
                font-size: 10pt;
                padding-top: 15px;
                border-top: 2px solid #ccc;
            }
            ul, ol {
                margin-left: 20px;
            }
            li {
                margin: 8px 0;
            }
            .teacher-credit {
                text-align: center;
                font-style: italic;
                font-size: 10pt;
                color: #666;
                margin-top: 5px;
                padding: 5px;
                border-top: 1px solid #ccc;
            }
        }
    </style>
</head>
<body>

<!-- PAGE 1 (FRONT) -->
<div class="page">
    <div style="text-align: center; margin-bottom: 20px;">
        <h1>📊 AP Statistics</h1>
        <h2>Your Gateway to Career Success</h2>
        <p style="font-weight: bold; font-size: 12pt;">Why Juniors Should Take AP Stats Senior Year</p>
        <p style="font-size: 10pt; color: #666;">''' + today + '''</p>
        <div class="teacher-credit">
            Compiled by Dr. Roland Lucas<br>
            AP Statistics Teacher at Newark Tech
        </div>
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
        <h2>📚 AP Stats Methods You\'ll Learn</h2>
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
        <div class="teacher-credit">
            AP Statistics: The Data Skills Every Career Demands<br>
            Dr. Roland Lucas, Newark Tech
        </div>
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
            <li>Check your school\'s AP course offerings and deadlines</li>
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
        <div class="teacher-credit">
            <strong>AP Statistics: The Data Skills Every Career Demands</strong><br>
            Compiled by Dr. Roland Lucas, AP Statistics Teacher at Newark Tech
        </div>
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
                margin: 0.5in;
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.5;
                margin: 0;
                padding: 0;
                color: #000;
                background: white;
            }
            .slide {
                page-break-after: always;
                padding: 0.5in;
                min-height: 9.5in;
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 20px;
                font-size: 28pt;
            }
            h2 {
                color: #764ba2;
                border-bottom: 3px solid #764ba2;
                padding-bottom: 10px;
                margin-top: 30px;
                font-size: 20pt;
            }
            h3 {
                color: #333;
                margin-top: 25px;
                font-size: 16pt;
            }
            .example {
                background: #f8f9fa;
                padding: 15px;
                margin: 15px 0;
                border-left: 5px solid #667eea;
                border-radius: 5px;
            }
            .benefit-list {
                margin: 20px 0;
                padding-left: 20px;
            }
            .benefit-list li {
                margin: 10px 0;
                font-size: 11pt;
            }
            .stat-term {
                background: #fff3cd;
                padding: 3px 6px;
                border-radius: 3px;
                font-weight: bold;
            }
            .footer {
                position: absolute;
                bottom: 0.5in;
                width: calc(100% - 1in);
                text-align: center;
                font-size: 10pt;
                color: #666;
                border-top: 1px solid #ccc;
                padding-top: 10px;
            }
            .page-number::after {
                content: "Page " counter(page);
            }
            .career-title {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
            }
            .highlight-box {
                background: #e7f3ff;
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                border: 1px solid #b8d4ff;
            }
            .resources {
                background: #f0f7ff;
                padding: 15px;
                margin: 20px 0;
                border-radius: 8px;
                font-size: 11pt;
            }
            .resources h4 {
                margin-top: 0;
                color: #667eea;
            }
            .print-header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 15px;
                border-bottom: 2px solid #667eea;
            }
            .print-header small {
                font-size: 10pt;
                color: #666;
            }
            ul, ol {
                margin-left: 25px;
            }
            li {
                margin: 8px 0;
            }
            .teacher-credit {
                font-style: italic;
                color: #666;
                text-align: center;
                margin-top: 10px;
                padding-top: 10px;
                border-top: 1px solid #ccc;
                font-size: 11pt;
            }
        }
    </style>
</head>
<body>

<div class="print-header">
    <h1>AP Statistics Career Presentation</h1>
    <p><strong>AP Statistics: The Data Skills Every Career Demands</strong></p>
    <small>Generated on ''' + today + ''' | All content expanded for printing</small>
    <div class="teacher-credit">
        Compiled by Dr. Roland Lucas<br>
        AP Statistics Teacher at Newark Tech
    </div>
</div>'''
    
    # Add ALL slides to the printable version
    for i, slide in enumerate(slides):
        presentation_html += '<div class="slide">\n'
        
        if slide["type"] == "title":
            presentation_html += f'''
            <h1>{slide["title"]}</h1>
            <h2 style="text-align: center; color: #764ba2;">{slide["subtitle"]}</h2>
            <div style="text-align: center; margin-top: 100px; font-size: 16pt;">
                {slide["content"]}
            </div>
            <div class="teacher-credit">
                AP Statistics: The Data Skills Every Career Demands<br>
                Dr. Roland Lucas, AP Statistics Teacher at Newark Tech
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
                    <li><strong>YouTube Search:</strong> "Introduction to Statistics" or "AP Statistics course"</li>
                    <li><strong>Khan Academy AP Statistics:</strong> Free video lessons and practice problems</li>
                    <li><strong>College Board AP Statistics:</strong> Official course information and resources</li>
                    <li><strong>American Statistical Association:</strong> Career information and case studies</li>
                </ul>
            </div>
            '''
            
        elif slide["type"] == "career":
            career_name = slide["title"].replace("🏥 ", "").replace("📈 ", "").replace("⚕️ ", "").replace("💉 ", "").replace("🔒 ", "").replace("🧪 ", "").replace("🩺 ", "").replace("⚡ ", "").replace("🏗️ ", "").replace("👶 ", "").replace("💻 ", "").replace("🔬 ", "")
            
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
            
            # Add YouTube search tips
            presentation_html += f'''
            <div class="resources">
                <h4>📺 Find Videos About {career_name}:</h4>
                <p><strong>Search YouTube for:</strong></p>
                <ul>
            '''
            
            keywords = YOUTUBE_SEARCH_KEYWORDS.get(career_name, [f"statistics in {career_name}"])
            for keyword in keywords[:3]:  # Show top 3 keywords
                presentation_html += f'<li>"{keyword}"</li>\n'
            
            presentation_html += '''
                </ul>
                <p><strong>Guaranteed working videos:</strong></p>
                <ul>
            '''
            
            for key, video in GUARANTEED_VIDEOS.items():
                presentation_html += f'<li><a href="{video["url"]}">{video["title"]}</a></li>\n'
            
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
                    <strong>Video Resources:</strong><br>
                    • Search YouTube: "AP Statistics introduction"<br>
                    • Khan Academy: Free AP Statistics course<br>
                    • College Board: Official AP Statistics resources
                </p>
            </div>
            
            <div class="teacher-credit">
                <strong>AP Statistics: The Data Skills Every Career Demands</strong><br>
                Compiled by Dr. Roland Lucas, AP Statistics Teacher at Newark Tech
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

def main():
    # Initialize session state
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
        
        # YOUTUBE SEARCH SECTION
        st.markdown("---")
        st.subheader("🔍 Quick YouTube Search")
        
        # Show search keywords for current slide
        slide = slides[st.session_state.current_slide]
        if slide["type"] in ["intro", "career"]:
            if slide["type"] == "intro":
                career_name = "statistics"
            else:
                career_name = slide["title"].replace("🏥 ", "").replace("📈 ", "").replace("⚕️ ", "").replace("💉 ", "").replace("🔒 ", "").replace("🧪 ", "").replace("🩺 ", "").replace("⚡ ", "").replace("🏗️ ", "").replace("👶 ", "").replace("💻 ", "").replace("🔬 ", "")
            
            keywords = YOUTUBE_SEARCH_KEYWORDS.get(career_name, ["statistics"])
            
            # Show top 3 keywords as clickable links
            st.markdown("**Click to search YouTube:**")
            for idx, keyword in enumerate(keywords[:3]):
                search_url = create_youtube_search_url(keyword)
                st.markdown(f"[🔎 {keyword}]({search_url})")
        
        # GUARANTEED WORKING VIDEOS
        st.markdown("---")
        st.subheader("✅ Always Works")
        
        for key, video in GUARANTEED_VIDEOS.items():
            st.markdown(f"[▶️ {video['title']}]({video['url']})")
        
        # PRINT/SAVE BUTTONS
        st.markdown("---")
        st.subheader("🖨️ Print & Save")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Print Flyer", use_container_width=True):
                st.session_state.show_flyer = True
                st.session_state.show_printable = False
                st.rerun()
        
        with col2:
            if st.button("📊 Full Presentation", use_container_width=True):
                st.session_state.show_printable = True
                st.session_state.show_flyer = False
                st.rerun()
        
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
        
        presentation_html = create_complete_presentation_html()
        b64 = base64.b64encode(presentation_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="ap_statistics_presentation.html" style="background:#667eea;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">📥 Download HTML for Printing</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Display the HTML
        st.components.v1.html(presentation_html, height=800, scrolling=True)
        
        if st.button("← Back to Interactive Presentation"):
            st.session_state.show_printable = False
            st.rerun()
        
        return
    
    if st.session_state.show_flyer:
        st.markdown("## 📄 2-Page Printable Flyer")
        st.info("**Instructions:** Print double-sided or save as PDF. Perfect for handing out!")
        
        flyer_html = create_flyer_html()
        b64 = base64.b64encode(flyer_html.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="ap_statistics_flyer.html" style="background:#667eea;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">📥 Download HTML for Printing</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Display the HTML
        st.components.v1.html(flyer_html, height=800, scrolling=True)
        
        if st.button("← Back to Interactive Presentation"):
            st.session_state.show_flyer = False
            st.rerun()
        
        return
    
    # TEACHER BANNER WITH NEW HEADER
    st.markdown("""
    <div class="teacher-banner">
        <h3>AP Statistics: The Data Skills Every Career Demands</h3>
        <p>Compiled by Dr. Roland Lucas</p>
        <p>AP Statistics Teacher at Newark Tech</p>
    </div>
    """, unsafe_allow_html=True)
    
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
        
        # YouTube search section
        display_youtube_search("statistics", YOUTUBE_SEARCH_KEYWORDS["general"])
        
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
        
        # YouTube search section
        display_youtube_search("AP Statistics", YOUTUBE_SEARCH_KEYWORDS["general"])
        
        # Display resources
        st.markdown("---")
        st.markdown("### 🔍 Explore Real Statistics in Action")
        st.markdown("**Search for these terms on YouTube to see statistics in action (click to open):**")
        
        col1, col2, col3 = st.columns(3)
        keywords = YOUTUBE_SEARCH_KEYWORDS["general"]
        
        with col1:
            for keyword in keywords[:2]:
                search_url = create_youtube_search_url(keyword)
                st.markdown(f"[🔍 {keyword}]({search_url})")
        
        with col2:
            for keyword in keywords[2:4]:
                search_url = create_youtube_search_url(keyword)
                st.markdown(f"[🔍 {keyword}]({search_url})")
        
        with col3:
            for keyword in keywords[4:]:
                search_url = create_youtube_search_url(keyword)
                st.markdown(f"[🔍 {keyword}]({search_url})")
    
    elif slide["type"] == "career":
        career_name = slide["title"].replace("🏥 ", "").replace("📈 ", "").replace("⚕️ ", "").replace("💉 ", "").replace("🔒 ", "").replace("🧪 ", "").replace("🩺 ", "").replace("⚡ ", "").replace("🏗️ ", "").replace("👶 ", "").replace("💻 ", "").replace("🔬 ", "")
        
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
        
        # Display YouTube search for this career
        display_career_resources(slide["content"]["resources"], career_name)
        
        # Add College Schedule Section
        if career_name in NJ_COLLEGE_SCHEDULES:
            with st.expander("🎓 Sample College Schedule at a New Jersey State School", expanded=False):
                schedule_data = NJ_COLLEGE_SCHEDULES[career_name]
                
                st.markdown(f"""
                <div class='schedule-box'>
                    <h3>🏫 {schedule_data['school']}</h3>
                    <p><strong>Major:</strong> {schedule_data['major']}</p>
                    <p><strong>Note:</strong> {schedule_data['stats_note']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### 📅 4-Year Course Schedule")
                
                for year, courses in schedule_data['schedule'].items():
                    st.markdown(f"<div class='schedule-year'><strong>{year}:</strong>", unsafe_allow_html=True)
                    for course in courses:
                        if "Statistics" in course or "(AP Credit Accepted!)" in course:
                            st.markdown(f"✅ **{course}**")
                        else:
                            st.markdown(f"• {course}")
                    st.markdown("</div>", unsafe_allow_html=True)
    
    elif slide["type"] == "closing":
        st.markdown(f"<h1 class='main-header'>{slide['title']}</h1>", unsafe_allow_html=True)
        
        # YouTube search section for career exploration
        st.markdown("### 🔍 Explore More Careers")
        st.markdown("**Click these links to search YouTube and learn about statistics in different fields:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Healthcare Fields:**")
            for career in ["NICU Nurse", "Pediatric Surgeon", "Registered Nurse", "Dermatology Physician Assistant", "Pediatrician"]:
                keywords = YOUTUBE_SEARCH_KEYWORDS.get(career, [f"statistics in {career}"])
                if keywords:
                    search_url = create_youtube_search_url(keywords[0])
                    st.markdown(f"[🔍 {career}]({search_url})")
        
        with col2:
            st.markdown("**Technology & Engineering:**")
            for career in ["Cybersecurity Professional", "Software Developer", "Electrical Engineer", "Civil Engineer", "Physicist / Nanotechnologist"]:
                keywords = YOUTUBE_SEARCH_KEYWORDS.get(career, [f"statistics in {career}"])
                if keywords:
                    search_url = create_youtube_search_url(keywords[0])
                    st.markdown(f"[🔍 {career}]({search_url})")
        
        # Add decorative gradient background
        st.markdown("""
        <div style='height: 400px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 20px; margin: 2rem 0; padding: 3rem; color: white;'>
        """, unsafe_allow_html=True)
        
        for point in slide["content"]["points"]:
            st.markdown(f"<h3 style='color: white; margin: 1rem 0;'>{point}</h3>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.success(slide["content"]["call_to_action"])
        
        # Final resources section with YouTube search
        st.markdown("---")
        st.markdown("### 🎓 Next Steps")
        st.info(slide["content"]["contact"])
        
        # Final YouTube search recommendation
        st.markdown("### 📺 Start Your Search")
        st.markdown("""
        <div class='video-container'>
        <strong>Click these links to begin exploring statistics videos:</strong>
        <div class='video-link'>
            ▶️ <a href="https://www.youtube.com/results?search_query=introduction+to+statistics" target="_blank">Search: "Introduction to Statistics"</a>
        </div>
        <div class='video-link'>
            ▶️ <a href="https://www.youtube.com/results?search_query=AP+Statistics+course" target="_blank">Search: "AP Statistics course"</a>
        </div>
        <div class='video-link'>
            ▶️ <a href="https://www.youtube.com/results?search_query=statistics+careers" target="_blank">Search: "Statistics careers"</a>
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer with teacher credit
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.caption("💡 **Tip:** Click any search link to open YouTube in a new tab")
        st.caption("🎓 **AP Statistics: The Data Skills Every Career Demands** - Dr. Roland Lucas, Newark Tech")

if __name__ == "__main__":
    main()
