import streamlit as st
import base64
from io import BytesIO

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
</style>
""", unsafe_allow_html=True)

# Career Resources Data
CAREER_RESOURCES = {
    "general": {
        "College Board AP Statistics": "https://apcentral.collegeboard.org/courses/ap-statistics",
        "American Statistical Association": "https://www.amstat.org/",
        "Khan Academy Statistics": "https://www.khanacademy.org/math/statistics-probability",
        "Stat Trek Statistics Tutorials": "https://stattrek.com/",
        "Bureau of Labor Statistics": "https://www.bls.gov/ooh/math/statisticians.htm",
    },
    "NICU Nurse": {
        "Nursing Statistics Resources": "https://www.nursingworld.org/practice-policy/workforce/what-is-nursing/",
        "Neonatal Nursing Info": "https://nann.org/education/what-is-neonatal-nursing",
        "Healthcare Data Analysis": "https://www.cdc.gov/nchs/index.htm",
        "Evidence-Based Nursing": "https://www.ebn.bmj.com/",
    },
    "Marketing Professional": {
        "Marketing Analytics Resources": "https://www.ama.org/marketing-analytics/",
        "Digital Marketing Statistics": "https://www.thinkwithgoogle.com/",
        "Consumer Behavior Research": "https://www.acrwebsite.org/",
        "Data-Driven Marketing": "https://www.marketingprofs.com/charts/category/18/data-driven-marketing",
    },
    "Pediatric Surgeon": {
        "Surgical Statistics": "https://www.facs.org/",
        "Pediatric Surgery Resources": "https://www.pedsurglibrary.com/",
        "Medical Research Statistics": "https://www.nih.gov/",
        "Clinical Trial Analysis": "https://clinicaltrials.gov/",
    },
    "Registered Nurse": {
        "Nursing Statistics Education": "https://www.nln.org/",
        "Healthcare Quality Metrics": "https://www.ahrq.gov/talkingquality/index.html",
        "Patient Safety Data": "https://www.psqh.com/",
        "Nursing Research": "https://www.nursingresearch.org/",
    },
    "Cybersecurity Professional": {
        "Cybersecurity Statistics": "https://www.sans.org/",
        "Security Data Analysis": "https://www.cisecurity.org/",
        "Threat Intelligence": "https://www.mitre.org/",
        "InfoSec Statistics": "https://www.isaca.org/resources/isaca-journal/issues",
    },
    "Cosmetic Scientist": {
        "Cosmetic Science Statistics": "https://www.scconline.org/",
        "Product Testing Methods": "https://www.astm.org/standards/cosmetic-and-personal-care-products.html",
        "Consumer Research Statistics": "https://www.quirks.com/",
        "Beauty Industry Data": "https://www.cosmeticsdesign.com/",
    },
    "Dermatology Physician Assistant": {
        "Dermatology Statistics": "https://www.aad.org/",
        "Medical Diagnostics": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5540140/",
        "Clinical Study Analysis": "https://www.jaad.org/",
        "Skin Cancer Statistics": "https://www.cancer.org/cancer/types/skin-cancer.html",
    },
    "Electrical Engineer": {
        "Engineering Statistics": "https://www.ieee.org/",
        "Quality Control Methods": "https://asq.org/",
        "Reliability Engineering": "https://www.weibull.com/",
        "Electrical Standards": "https://www.nema.org/standards",
    },
    "Civil Engineer": {
        "Structural Statistics": "https://www.asce.org/",
        "Construction Data Analysis": "https://www.agc.org/",
        "Materials Testing Standards": "https://www.astm.org/",
        "Infrastructure Statistics": "https://www.infrastructurereportcard.org/",
    },
    "Pediatrician": {
        "Pediatric Growth Charts": "https://www.cdc.gov/growthcharts/",
        "Child Health Statistics": "https://www.aap.org/en/patient-care/",
        "Clinical Evidence": "https://www.cochrane.org/",
        "Vaccine Statistics": "https://www.cdc.gov/vaccines/index.html",
    },
    "Software Developer": {
        "A/B Testing Resources": "https://www.optimizely.com/optimization-glossary/ab-testing/",
        "Machine Learning Statistics": "https://www.kaggle.com/learn/statistics",
        "Data Science Education": "https://www.datacamp.com/courses/statistics-fundamentals",
        "Tech Industry Data": "https://stackoverflow.blog/",
    },
    "Physicist / Nanotechnologist": {
        "Physics Statistics": "https://www.aps.org/",
        "Nanotechnology Research": "https://www.nano.gov/",
        "Experimental Design": "https://www.physicsforums.com/",
        "Scientific Data Analysis": "https://www.nature.com/subjects/data-analysis",
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

def display_resources(career_key):
    """Display resource links for a specific career"""
    if career_key in CAREER_RESOURCES:
        st.markdown("### 🔗 Learn More & Resources")
        st.markdown("Explore these resources to learn how statistics applies to this career:")
        
        resources = CAREER_RESOURCES[career_key]
        for name, url in resources.items():
            st.markdown(f"""
            <div class='resource-link'>
                📚 <a href='{url}' target='_blank'>{name}</a>
            </div>
            """, unsafe_allow_html=True)
        
        # Also show general resources if this is a specific career
        if career_key != "general":
            st.markdown("---")
            st.markdown("#### General AP Statistics Resources")
            general_resources = CAREER_RESOURCES["general"]
            for name, url in list(general_resources.items())[:3]:  # Show only top 3
                st.markdown(f"• [{name}]({url})", unsafe_allow_html=True)

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
        
        # Resource Links Section
        st.markdown("---")
        st.subheader("🔗 Quick Resource Links")
        
        # Display relevant resources based on current slide
        slide = slides[st.session_state.current_slide]
        if slide["type"] in ["intro", "career"] and "resources" in slide["content"]:
            career_key = slide["content"]["resources"]
            if career_key in CAREER_RESOURCES:
                resources = CAREER_RESOURCES[career_key]
                for name, url in list(resources.items())[:2]:  # Show top 2 in sidebar
                    st.markdown(f"[{name}]({url})")
        
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
        
        # Quick AP Stats info
        st.markdown("---")
        st.subheader("AP Statistics Info")
        st.markdown("[College Board AP Stats](https://apcentral.collegeboard.org/courses/ap-statistics)")
        st.markdown("[AP Stats Course Guide](https://apstudents.collegeboard.org/courses/ap-statistics)")
        st.markdown("[AP Stats Practice Tests](https://www.khanacademy.org/math/ap-statistics)")
    
    # Main content area
    slide = slides[st.session_state.current_slide]
    
    # Display slide based on type
    if slide["type"] == "title":
        st.markdown(f"<h1 class='main-header'>{slide['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='sub-header'>{slide['subtitle']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: #667eea; margin-top: 2rem;'>{slide['content']}</h3>", unsafe_allow_html=True)
        
        # Add resource box
        with st.expander("📚 Quick Start Resources"):
            st.markdown("""
            **Start your AP Statistics journey with these resources:**
            - [Official College Board AP Statistics Page](https://apcentral.collegeboard.org/courses/ap-statistics)
            - [Khan Academy AP Statistics Course](https://www.khanacademy.org/math/ap-statistics)
            - [AP Statistics Student Guide](https://apstudents.collegeboard.org/courses/ap-statistics)
            - [Statistics Career Information](https://www.amstat.org/asa/education/Career-Paths-for-Statisticians.aspx)
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
        
        # Display general resources
        st.markdown("---")
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
        
        # Display career-specific resources
        if "resources" in slide["content"]:
            display_resources(slide["content"]["resources"])
    
    elif slide["type"] == "closing":
        st.markdown(f"<h1 class='main-header'>{slide['title']}</h1>", unsafe_allow_html=True)
        
        # Add resource section before closing
        with st.expander("🎓 Next Steps & Resources", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**AP Statistics Resources:**")
                st.markdown("""
                - [College Board AP Stats](https://apcentral.collegeboard.org/courses/ap-statistics)
                - [AP Stats Course Overview](https://apstudents.collegeboard.org/courses/ap-statistics)
                - [Practice Questions & Tests](https://www.khanacademy.org/math/ap-statistics)
                - [Statistics Career Paths](https://www.amstat.org/asa/education/Career-Paths-for-Statisticians.aspx)
                """)
            
            with col2:
                st.markdown("**College Planning:**")
                st.markdown("""
                - [College Majors Requiring Stats](https://www.collegeboard.org/)
                - [Statistics in College Admissions](https://blog.collegeboard.org/)
                - [Career Exploration Tools](https://www.bls.gov/ooh/math/statisticians.htm)
                - [STEM Career Resources](https://www.ed.gov/stem)
                """)
        
        # Add decorative gradient background
        st.markdown("""
        <div style='height: 400px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        border-radius: 20px; margin: 2rem 0; padding: 3rem; color: white;'>
        """, unsafe_allow_html=True)
        
        for point in slide["content"]["points"]:
            st.markdown(f"<h3 style='color: white; margin: 1rem 0;'>{point}</h3>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.success(slide["content"]["call_to_action"])
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
