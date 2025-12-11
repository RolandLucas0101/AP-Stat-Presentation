import streamlit as st
import base64
import urllib.parse
from datetime import datetime

# --- Page config ---
st.set_page_config(page_title="AP Statistics — Careers & Live YouTube Search", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# --- Styles ---
st.markdown("""
<style>
.main-header {font-size: 2.2rem; color: #2b3a67; text-align: center; margin-bottom: 0.5rem; font-weight: 700;}
.sub-header {font-size: 1.1rem; color: #764ba2; text-align: center; margin-bottom: 1rem;}
.slide-card {background: linear-gradient(135deg, #f5f7fa 0%, #cfe3ff 100%); padding: 1rem; border-radius: 12px; margin: 8px 0;}
.example-box {background: white; padding: 1rem; border-radius: 8px; margin: 8px 0; border-left: 4px solid #667eea;}
.resource-link {background: #eef6ff; padding: 0.6rem; border-radius: 6px; margin: 6px 0; border-left: 4px solid #667eea;}
.video-container {margin: 0.5rem 0; padding: 0.6rem; background: #f0f8ff; border-radius: 8px; border-left: 4px solid #ff6b6b;}
.schedule-box {background: linear-gradient(135deg, #f0f7ff, #e6f2ff); padding: 0.8rem; border-radius: 8px; margin: 6px 0; border: 1px solid #cfdfff;}
</style>
""", unsafe_allow_html=True)

# --- Data: careers, videos, keywords, resources ---
CAREERS = [
    "NICU Nurse", "Marketing Professional", "Pediatric Surgeon", "Registered Nurse",
    "Cybersecurity Professional", "Cosmetic Scientist", "Dermatology Physician Assistant",
    "Electrical Engineer", "Civil Engineer", "Pediatrician", "Software Developer",
    "Physicist / Nanotechnologist"
]

# Verified fallback video IDs (replace as you discover better exemplars)
VERIFIED_VIDEOS = {
    "NICU Nurse": "UFZ3o6z3DlA",
    "Marketing Professional": "MunG48LH_hs",
    "Pediatric Surgeon": "MynqBaooqus",
    "Registered Nurse": "UFZ3o6z3DlA",
    "Cybersecurity Professional": "n8e3-vw_TbU",
    "Cosmetic Scientist": "n8e3-vw_TbU",
    "Dermatology Physician Assistant": "MynqBaooqus",
    "Electrical Engineer": "n8e3-vw_TbU",
    "Civil Engineer": "n8e3-vw_TbU",
    "Pediatrician": "MynqBaooqus",
    "Software Developer": "kyjlxsLW1Is",
    "Physicist / Nanotechnologist": "GUQJ7zMoSCM"
}

# Suggested YouTube search keywords per career
YOUTUBE_KEYWORDS = {
    "NICU Nurse": ["statistics in neonatal care","NICU nursing data analysis","clinical NICU outcomes statistics"],
    "Marketing Professional": ["marketing analytics tutorial","A/B testing marketing beginners","customer segmentation tutorial"],
    "Pediatric Surgeon": ["pediatric clinical trials statistics","surgical outcomes statistics","biostatistics for surgeons"],
    "Registered Nurse": ["nursing research statistics","quality improvement nursing statistics","interpret lab results statistics"],
    "Cybersecurity Professional": ["security analytics tutorial","anomaly detection statistics","threat modeling statistics"],
    "Cosmetic Scientist": ["cosmetic product testing statistics","formulation optimization statistics","consumer testing cosmetics statistics"],
    "Dermatology Physician Assistant": ["dermatology sensitivity specificity","diagnostic test statistics dermatology","clinical research dermatology statistics"],
    "Electrical Engineer": ["engineering statistics reliability testing","quality control statistics electrical","survival analysis components"],
    "Civil Engineer": ["structural safety statistics","materials testing statistics civil","load probability analysis bridge design"],
    "Pediatrician": ["growth chart percentiles statistics","vaccine efficacy statistics pediatric","pediatric clinical research statistics"],
    "Software Developer": ["A/B testing tutorial developers","experiment design software features","metrics and analytics for developers"],
    "Physicist / Nanotechnologist": ["statistical mechanics primer","data analysis experimental physics","uncertainty propagation physics"]
}

# Simple career blurbs and examples used in slides
CAREER_BLURBS = {
    "NICU Nurse": "NICU nurses use statistics to track vital signs, evaluate treatments, and monitor infection rates.",
    "Marketing Professional": "Marketers use statistics for A/B testing, segmentation, and ROI measurement.",
    "Pediatric Surgeon": "Surgeons rely on statistics for outcome prediction, clinical research, and risk modeling.",
    "Registered Nurse": "Nurses use statistics for lab interpretation, quality improvement, and patient monitoring.",
    "Cybersecurity Professional": "Security analysts use statistics for anomaly detection and threat modeling.",
    "Cosmetic Scientist": "Scientists use statistics for product testing, stability analysis, and consumer trials.",
    "Dermatology Physician Assistant": "PAs use sensitivity/specificity and clinical trial interpretation for diagnostics.",
    "Electrical Engineer": "Engineers use statistics for reliability testing, QC, and predictive maintenance.",
    "Civil Engineer": "Civil engineers use stats for load analysis, materials testing, and safety margins.",
    "Pediatrician": "Pediatricians use growth percentiles, vaccine stats, and clinical study interpretation.",
    "Software Developer": "Developers use A/B testing, model evaluation, and metrics to guide product decisions.",
    "Physicist / Nanotechnologist": "Physicists use error analysis, hypothesis testing, and data modeling."
}

EXAMPLE_CASES = {
    "NICU Nurse": ["Analyze heart rate trends (mean, SD) to spot early distress.", "Compare feeding protocols with hypothesis tests."],
    "Marketing Professional": ["A/B test subject lines and measure conversions (proportions & CI).", "Segment customers with clustering methods."],
    "Pediatric Surgeon": ["Use regression to predict operative time.", "Design randomized studies comparing techniques."],
}

# NJ college schedules excerpt (kept concise)
NJ_COLLEGE_SCHEDULES = {
    "NICU Nurse": {"school":"Rutgers School of Nursing","stats":"Statistics for Healthcare","years":["Year1: Bio, Chem, Writing","Year2: Anatomy, Micro, Statistics","Year3: Nursing Fundamentals","Year4: Clinical Capstone"]},
    "Marketing Professional": {"school":"Rutgers Business School","stats":"Business Statistics","years":["Year1: Intro to Business, Calc","Year2: Consumer Behavior, Business Stats","Year3: Marketing Research","Year4: Capstone & Internship"]},
    "Pediatrician": {"school":"Rutgers - Pre-med","stats":"Statistics for Biology","years":["Year1: Bio & Chem","Year2: Organic Chem & Physics","Year3: Biochem & Research Methods","Year4: MCAT Prep & Electives"]},
    # other careers omitted for brevity but can be added similarly
}

# --- Helper functions ---
def build_youtube_search_url(query: str) -> str:
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.youtube.com/results?search_query={encoded}"

def youtube_watch_url(video_id: str) -> str:
    return f"https://www.youtube.com/watch?v={video_id}"

def create_flyer_html(today=None):
    if today is None:
        today = datetime.now().strftime("%B %d, %Y")
    return f\"\"\"<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>AP Statistics Flyer</title></head><body>
<h1>AP Statistics — Career Connections</h1>
<p>Generated: {today}</p>
<p>Take AP Statistics to prepare for college and careers that rely on data.</p>
</body></html>\"\"\"

# --- Slides data (title, intro, career slides, closing) ---
slides = [
    {"type":"title","title":"📊 AP Statistics","subtitle":"Your Gateway to Career Success","content":"Why Juniors Should Take AP Statistics Senior Year"},
    {"type":"intro","title":"Why AP Statistics Matters","content":{"benefits":["Required for many majors","College credit potential","Career-ready data skills"],"applications":"AP Stats builds foundational skills used across professions.","resources":"general"}},
]

# add career slides programmatically
for career in CAREERS:
    slides.append({
        "type":"career",
        "title":career,
        "content":{"description":CAREER_BLURBS.get(career,""), "examples":[{"title":ex,"content":""} for ex in EXAMPLE_CASES.get(career, ["Practice hypothesis testing with class data.","Work on regression projects."])], "resources":career, "youtube_video": VERIFIED_VIDEOS.get(career)}
    })

slides.append({"type":"closing","title":"Take AP Statistics Next Year!","content":{"points":["Prepare for any college major","Gain real-world data skills","Earn possible college credit"],"call_to_action":"Register during course selection","contact":"Talk to your guidance counselor"}})

# --- Main app ---
def main():
    if 'current_slide' not in st.session_state:
        st.session_state.current_slide = 0
    if 'show_printable' not in st.session_state:
        st.session_state.show_printable = False
    if 'show_flyer' not in st.session_state:
        st.session_state.show_flyer = False

    # Sidebar
    with st.sidebar:
        st.title("📋 Navigation")
        slide_options = [f\"Slide {i+1}: {slides[i]['title']}\" for i in range(len(slides))]
        selected = st.selectbox(\"Go to slide\", slide_options, index=st.session_state.current_slide)
        st.session_state.current_slide = int(selected.split(':')[0].replace('Slide ','') ) - 1

        st.markdown('---')
        st.write('Printable / downloads')
        if st.button('Download 2-page flyer'):
            html = create_flyer_html()
            b64 = base64.b64encode(html.encode()).decode()
            href = f'<a href=\"data:text/html;base64,{b64}\" download=\"ap_stats_flyer.html\">Download flyer HTML</a>'
            st.markdown(href, unsafe_allow_html=True)

        if st.button('Download full presentation (HTML)'):
            # build a small presentation HTML
            pres = '<html><body>' + ''.join([f\"<h1>{s['title']}</h1>\" for s in slides]) + '</body></html>'
            b64 = base64.b64encode(pres.encode()).decode()
            href = f'<a href=\"data:text/html;base64,{b64}\" download=\"ap_stats_presentation.html\">Download presentation HTML</a>'
            st.markdown(href, unsafe_allow_html=True)

        st.markdown('---')
        st.write('Quick resources')
        st.markdown('- [AP Statistics (College Board)](https://apcentral.collegeboard.org/courses/ap-statistics)')
        st.markdown('- [Khan Academy - Statistics](https://www.khanacademy.org/math/statistics-probability)')
        st.markdown('---')
        st.caption('Video tools integrated into each career slide — pick a keyword or type your own and open YouTube search.')

    # Top area
    st.markdown(f\"<h1 class='main-header'>{slides[st.session_state.current_slide]['title']}</h1>\", unsafe_allow_html=True)
    current = slides[st.session_state.current_slide]

    # Printable / flyer views
    if st.session_state.show_printable:
        st.markdown('## Printable Presentation (HTML)')
        pres_html = '<html><body>' + ''.join([f\"<h1>{s['title']}</h1><div>{s.get('content','')}</div>\" for s in slides]) + '</body></html>'
        st.components.v1.html(pres_html, height=700, scrolling=True)
        if st.button('Back to presentation'):
            st.session_state.show_printable = False
            st.experimental_rerun()
        return

    if st.session_state.show_flyer:
        st.markdown('## 2-Page Flyer')
        flyer = create_flyer_html()
        st.components.v1.html(flyer, height=600, scrolling=True)
        if st.button('Back to presentation'):
            st.session_state.show_flyer = False
            st.experimental_rerun()
        return

    # Show slide content
    if current['type'] == 'title':
        st.markdown(f\"<h2 class='sub-header'>{current.get('subtitle','')}</h2>\", unsafe_allow_html=True)
        st.write(current.get('content',''))

    elif current['type'] == 'intro':
        st.subheader(current['title'])
        for b in current['content'].get('benefits',[]):
            st.markdown(f\"- {b}\")
        st.info(current['content'].get('applications',''))

    elif current['type'] == 'career':
        career_name = current['title']
        st.subheader(career_name)
        st.markdown(f\"<div class='slide-card'><strong>Description:</strong> {current['content'].get('description','')}</div>\", unsafe_allow_html=True)

        # examples
        st.markdown('### Examples')
        for ex in current['content'].get('examples',[]):
            st.markdown(f\"- {ex.get('title','')}\")

        # college schedule if present
        if career_name in NJ_COLLEGE_SCHEDULES:
            info = NJ_COLLEGE_SCHEDULES[career_name]
            st.markdown('### Sample NJ College Path')
            st.markdown(f\"**{info['school']}** — Required stats course: *{info['stats']}*\" )
            for y in info['years']:
                st.markdown(f\"- {y}\")

        st.markdown('---')

        # VIDEO & SEARCH PANEL (integrated into slide)
        st.markdown('### 🎥 Video & YouTube Search')
        col1, col2 = st.columns([2,1])

        # left: verified video embed + link
        with col1:
            vid_id = current['content'].get('youtube_video') or VERIFIED_VIDEOS.get(career_name)
            if vid_id:
                # show embedded player and link to YouTube
                try:
                    st.video(youtube_watch_url(vid_id))
                except Exception:
                    st.markdown(f\"[Watch example video]({youtube_watch_url(vid_id)})\")
            else:
                st.write('No verified example video available. Use search below.')

            st.markdown('**Teacher tip:** Replace the verified video ID in the repo with a local favourite to keep your class examples stable.')

        # right: keywords, custom search, open URL
        with col2:
            st.markdown('Suggested search keywords (pick one or type your own)')
            kws = YOUTUBE_KEYWORDS.get(career_name, [])
            if kws:
                sel_kw = st.selectbox('Choose keyword', [''] + kws, key=f'kw_{career_name}')
            else:
                sel_kw = ''

            custom = st.text_input('Or type a search phrase', value='', key=f'custom_{career_name}')
            final_query = (custom.strip() if custom.strip() else sel_kw.strip()).strip()
            if final_query == '':
                final_query = career_name  # fallback to career name

            search_url = build_youtube_search_url(f\"{career_name} {final_query}\")
            if st.button('🔎 Open YouTube search results', key=f'open_{career_name}'):
                st.markdown(f\"[Open YouTube results for: {urllib.parse.unquote_plus(final_query)}]({search_url})\", unsafe_allow_html=True)
            if st.button('📋 Copy search URL', key=f'copy_{career_name}'):
                st.write(search_url)

    elif current['type'] == 'closing':
        st.subheader(current['title'])
        for p in current['content'].get('points',[]):
            st.markdown(f\"- {p}\")
        st.markdown(f\"**{current['content'].get('call_to_action','')}**\")
        st.markdown(current['content'].get('contact',''))

    # Bottom navigation buttons
    coln1, coln2, coln3 = st.columns([1,1,4])
    with coln1:
        if st.button('◀ Previous', disabled=st.session_state.current_slide==0):
            st.session_state.current_slide = max(0, st.session_state.current_slide - 1)
            st.experimental_rerun()
    with coln2:
        if st.button('Next ▶', disabled=st.session_state.current_slide==len(slides)-1):
            st.session_state.current_slide = min(len(slides)-1, st.session_state.current_slide + 1)
            st.experimental_rerun()

    # Footer tools
    st.markdown('---')
    st.write('Classroom exports:')
    c1, c2 = st.columns(2)
    with c1:
        # download keywords CSV
        import io, csv
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['career','keyword'])
        for c, kws in YOUTUBE_KEYWORDS.items():
            for k in kws:
                writer.writerow([c, k])
        st.download_button('Download keywords CSV', output.getvalue(), 'youtube_keywords.csv', 'text/csv')
    with c2:
        # mini flyer
        flyer_html = create_flyer_html()
        b64 = base64.b64encode(flyer_html.encode()).decode()
        href = f'<a href=\"data:text/html;base64,{b64}\" download=\"ap_stats_flyer.html\">Download mini flyer (HTML)</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
