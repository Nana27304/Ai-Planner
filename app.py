import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import json, os, random, math

st.set_page_config(page_title="PlanningAI - Emmanuel Gyasi", page_icon="🎓", layout="wide")

# --- SAVE ---
def load(name, default):
    if os.path.exists(name):
        try:
            with open(name) as f: return json.load(f)
        except: return default
    return default

def save(name, data):
    with open(name, "w") as f: json.dump(data, f)

tasks = load("tasks.json", [])
timetable = load("timetable.json", [])
exams = load("exams.json", [])

st.title("🎓 PlanningAI")
st.caption("Built by Emmanuel Gyasi | KNUST | Plan Smart, Achieve More")

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "📊 Dashboard", "✅ Smart Planner", "👥 Sample & Population",
    "🌍 Land Use", "📝 Brief Generator", "💼 Career",
    "🗓️ Timetable", "⏳ Exam Countdown", "🧠 AI Planner"
])

# 1. DASHBOARD
with tab1:
    done = len([t for t in tasks if t.get("done")])
    total = len(tasks)
    pct = int(done/total*100) if total else 0
    c1,c2,c3 = st.columns(3)
    c1.metric("Total Tasks", total)
    c2.metric("Completed", done)
    c3.metric("Progress", f"{pct}%")
    st.progress(pct/100)
    st.subheader("💡 Motivation Zone")
    quotes = [
        "Success is the sum of small efforts repeated day in and day out.",
        "Don't watch the clock, do what it does. Keep going.",
        "KNUST will remember your name if you don't give up.",
        "Plan your work, work your plan."
    ]
    st.info(random.choice(quotes))
    st.success("Welcome back, Emmanuel!")

# 2. PLANNER
with tab2:
    st.subheader("Add New Task")
    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("Task Title - e.g. Study MATH 151")
        cat = st.selectbox("Category", ["Study", "Assignment", "Project", "Personal", "Exam Prep"])
        due = st.date_input("Due Date", date.today())
        if st.form_submit_button("➕ Add Task"):
            if title:
                tasks.append({"title": title, "cat": cat, "due": str(due), "done": False})
                save("tasks.json", tasks); st.success("Task added!"); st.rerun()
    for i, t in enumerate(tasks):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        checked = col1.checkbox("", value=t["done"], key=f"t{i}")
        if checked != t["done"]:
            tasks[i]["done"] = checked; save("tasks.json", tasks); st.rerun()
        col2.write(f"**{t['title']}** - {t['cat']} | Due: {t['due']}")
        if col3.button("🗑️", key=f"d{i}"):
            tasks.pop(i); save("tasks.json", tasks); st.rerun()

# 3. SAMPLE & POPULATION - RESTORED
with tab3:
    st.subheader("👥 Sample & Population Calculator")
    st.write("For your Planning / Research project - Calculate sample size from population.")
    pop = st.number_input("Total Population - e.g. Population of Kumasi / KNUST students", min_value=10, value=1000, step=10)
    margin = st.slider("Margin of Error (%)", 1, 10, 5)
    confidence = st.selectbox("Confidence Level", ["90% - Z=1.645", "95% - Z=1.96", "99% - Z=2.576"])
    z_map = {"90% - Z=1.645": 1.645, "95% - Z=1.96": 1.96, "99% - Z=2.576": 2.576}
    z = z_map[confidence]
    p = 0.5
    e = margin/100
    # Cochran + finite population correction
    n0 = (z**2 * p * (1-p)) / (e**2)
    n = n0 / (1 + (n0-1)/pop)
    n = math.ceil(n)
    st.metric("Recommended Sample Size", n)
    st.info(f"From a population of {pop}, you should survey at least **{n} people** at {confidence} confidence and {margin}% error.")
    st.write("**How to use:** If population = 5000 students, sample = ~357. Use this in your project methodology.")
    st.bar_chart(pd.DataFrame({"Population": [pop], "Sample": [n]}))

# 4. LAND USE - RESTORED
with tab4:
    st.subheader("🌍 Land Use Planner")
    st.write("Plan land use for a community / site - like your Planning studio project.")
    total_land = st.number_input("Total Land Area (Hectares)", min_value=1.0, value=100.0)
    st.write("Allocate % for each use (must total 100%)")
    c1,c2,c3,c4 = st.columns(4)
    res = c1.slider("Residential %", 0, 100, 40)
    com = c2.slider("Commercial %", 0, 100, 15)
    green = c3.slider("Green / Open Space %", 0, 100, 20)
    road = c4.slider("Roads & Infra %", 0, 100, 15)
    other = 100 - (res+com+green+road)
    st.write(f"Remaining for Other / Institutional: **{other}%**")
    if other < 0:
        st.error("Total is over 100%! Reduce one.")
    else:
        data = {
            "Use": ["Residential","Commercial","Green Space","Roads","Other"],
            "Area (Ha)": [total_land*res/100, total_land*com/100, total_land*green/100, total_land*road/100, total_land*other/100]
        }
        df = pd.DataFrame(data)
        st.table(df)
        st.bar_chart(df.set_index("Use"))
        st.success(f"For {total_land} Ha: Residential = {total_land*res/100:.1f} Ha, Green = {total_land*green/100:.1f} Ha")

# 5. BRIEF GENERATOR - RESTORED
with tab5:
    st.subheader("📝 Brief Generator")
    st.write("Generate a project brief in 10 seconds for your Planning assignment.")
    proj_title = st.text_input("Project Title", "Redevelopment of Kejetia Market Area, Kumasi")
    location = st.text_input("Location", "Kumasi, Ashanti Region")
    problem = st.text_area("Problem / Issue", "Traffic congestion, poor drainage, informal trading blocking access")
    goal = st.text_area("Goal / Objective", "Create a safe, walkable, clean market area with proper drainage and parking")
    if st.button("✨ Generate Brief"):
        brief = f"""
        **PROJECT BRIEF: {proj_title}**

        **1. Location:** {location}
        **2. Background / Problem:** {problem}
        **3. Objective:** {goal}
        **4. Scope:** Site analysis, stakeholder consultation, land use plan, infrastructure proposal, implementation phasing.
        **5. Expected Outcome:** A sustainable, inclusive plan that improves livelihoods, mobility and environmental quality for residents and traders.
        **6. Methodology:** Field survey, population & sample survey, land use mapping, community engagement, GIS analysis.
        **7. Deliverables:** Report, Maps, Site Plan, Presentation.

        *Generated by PlanningAI - Emmanuel Gyasi*
        """
        st.markdown(brief)
        st.success("Copy this brief into your Word / Report!")

# 6. CAREER - RESTORED
with tab6:
    st.subheader("💼 Career Planner")
    st.write("Plan your career after KNUST - Planning, GIS, Urban Design.")
    interest = st.selectbox("What do you love most?", ["Urban Planning", "GIS & Mapping", "Real Estate", "Environmental Planning", "Transport Planning", "Research / Academia"])
    careers = {
        "Urban Planning": ["District Planner at District Assembly", "Urban Planner at Town & Country Planning Dept", "Consultant at Private Planning Firm"],
        "GIS & Mapping": ["GIS Analyst", "Remote Sensing Specialist", "Land Survey / Mapping Officer"],
        "Real Estate": ["Estate Manager", "Valuation Officer", "Property Developer"],
        "Environmental Planning": ["Environmental Officer at EPA", "Sustainability Consultant", "Climate Adaptation Planner"],
        "Transport Planning": ["Transport Planner at GHA / Urban Roads", "Traffic Engineer", "Mobility Consultant"],
        "Research / Academia": ["Teaching Assistant at KNUST", "Research Assistant", "MPhil / PhD in Planning"],
    }
    st.write(f"**Top 3 Careers for {interest}:**")
    for c in careers[interest]:
        st.write(f"- ✅ {c}")
    st.info("**Next Step:** Learn QGIS + AutoCAD + Excel. Build 3 projects in your portfolio. Apply for internship in Year 3.")

# 7. TIMETABLE - NEW
with tab7:
    st.subheader("🗓️ My KNUST Timetable")
    with st.form("tt_form", clear_on_submit=True):
        day = st.selectbox("Day", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        course = st.text_input("Course - e.g. MATH 151")
        start = st.time_input("Start", time(8,0))
        end = st.time_input("End", time(10,0))
        venue = st.text_input("Venue - e.g. PB 101")
        if st.form_submit_button("➕ Add To Timetable"):
            if course:
                timetable.append({"day":day,"course":course,"start":str(start),"end":str(end),"venue":venue})
                save("timetable.json", timetable); st.rerun()
    if timetable:
        for d in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
            dd = [x for x in timetable if x["day"]==d]
            if dd:
                st.markdown(f"**{d}**")
                st.table(pd.DataFrame(dd)[["course","start","end","venue"]])
    else:
        st.info("No classes yet. Add your lectures!")

# 8. EXAM COUNTDOWN - NEW
with tab8:
    st.subheader("⏳ Exam Countdown")
    with st.form("exam_form", clear_on_submit=True):
        exam_name = st.text_input("Exam - e.g. MATH 151 Mid-Sem")
        exam_date = st.date_input("Exam Date", date.today())
        if st.form_submit_button("➕ Add Exam"):
            if exam_name:
                exams.append({"name":exam_name,"date":str(exam_date)})
                save("exams.json", exams); st.rerun()
    today = date.today()
    for i, e in enumerate(exams):
        ed = date.fromisoformat(e["date"])
        days_left = (ed - today).days
        c1,c2,c3 = st.columns([0.5,0.3,0.2])
        c1.write(f"**{e['name']}** - {e['date']}")
        if days_left < 0: c2.error(f"Done {-days_left} days ago")
        elif days_left == 0: c2.warning("🔥 TODAY!")
        elif days_left <= 7: c2.warning(f"⚠️ {days_left} days left!")
        else: c2.success(f"✅ {days_left} days left")
        if c3.button("🗑️", key=f"ex{i}"):
            exams.pop(i); save("exams.json", exams); st.rerun()

# 9. AI PLANNER - RESTORED
with tab9:
    st.subheader("🧠 AI Planner")
    st.info("AI is paused for now - we will connect it later. No key needed for other tabs.")
    st.text_area("What do you want to plan?", placeholder="e.g. I have 3 exams next week...")
    if st.button("Ask AI Brain (Coming Soon)"):
        st.warning("We will add Groq / Google key later. Use Planner + Brief Generator for now!")