import streamlit as st
import pandas as pd
from datetime import date, time
import json
import os
import random
import math

st.set_page_config(page_title="AI Planner Ghana - Emmanuel Gyasi", page_icon="brain", layout="wide")

# ---------- GHANA DATA - ALL 16 REGIONS ----------
GHANA_DATA = {
    "Ashanti": {"capital": "Kumasi", "pop": 5431373, "districts": ["Kumasi", "Obuasi", "Mampong", "Ejisu", "Konongo", "Bekwai", "Offinso"]},
    "Greater Accra": {"capital": "Accra", "pop": 5601108, "districts": ["Accra", "Tema", "Madina", "Kasoa", "Achimota", "Legon", "Spintex"]},
    "Northern": {"capital": "Tamale", "pop": 2338265, "districts": ["Tamale", "Yendi", "Savelugu", "Gushegu", "Tolon", "Kumbungu"]},
    "Western": {"capital": "Sekondi-Takoradi", "pop": 2106584, "districts": ["Takoradi", "Sekondi", "Tarkwa", "Axim", "Elubo", "Prestea"]},
    "Western North": {"capital": "Sefwi Wiawso", "pop": 956300, "districts": ["Sefwi Wiawso", "Bibiani", "Juaboso", "Enchi"]},
    "Central": {"capital": "Cape Coast", "pop": 2860921, "districts": ["Cape Coast", "Winneba", "Kasoa", "Elmina", "Swedru", "Saltpond"]},
    "Eastern": {"capital": "Koforidua", "pop": 2906274, "districts": ["Koforidua", "Nkawkaw", "Akosombo", "Somanya", "Nsawam", "Kibi"]},
    "Volta": {"capital": "Ho", "pop": 1633363, "districts": ["Ho", "Hohoe", "Keta", "Aflao", "Kpando", "Sogakope"]},
    "Oti": {"capital": "Dambai", "pop": 747200, "districts": ["Dambai", "Jasikan", "Kadjebi", "Nkwanta"]},
    "Upper East": {"capital": "Bolgatanga", "pop": 1301451, "districts": ["Bolgatanga", "Bawku", "Navrongo", "Paga", "Bongo"]},
    "Upper West": {"capital": "Wa", "pop": 901100, "districts": ["Wa", "Lawra", "Jirapa", "Tumu", "Nadowli"]},
    "Savannah": {"capital": "Damongo", "pop": 653000, "districts": ["Damongo", "Bole", "Salaga", "Sawla"]},
    "North East": {"capital": "Nalerigu", "pop": 658900, "districts": ["Nalerigu", "Walewale", "Gambaga", "Bunkpurugu"]},
    "Bono": {"capital": "Sunyani", "pop": 1208432, "districts": ["Sunyani", "Berekum", "Dormaa", "Wenchi", "Techiman"]},
    "Bono East": {"capital": "Techiman", "pop": 1200000, "districts": ["Techiman", "Kintampo", "Atebubu", "Nkoranza", "Yeji"]},
    "Ahafo": {"capital": "Goaso", "pop": 564700, "districts": ["Goaso", "Bechem", "Duayaw Nkwanta", "Kenyasi"]}
}

def load(name, default):
    if os.path.exists(name):
        try:
            with open(name) as f:
                return json.load(f)
        except:
            return default
    return default

def save(name, data):
    with open(name, "w") as f:
        json.dump(data, f)

tasks = load("tasks.json", [])
timetable = load("timetable.json", [])
exams = load("exams.json", [])

# ---------- SIDEBAR - GHANA SELECTOR ----------
st.sidebar.title("Ghana Location")
st.sidebar.write("Select your location. App will adapt to you.")
region = st.sidebar.selectbox("Choose Your Region", list(GHANA_DATA.keys()), index=0)
districts_list = GHANA_DATA[region]["districts"]
district = st.sidebar.selectbox("Choose Your District / Town", districts_list)
capital = GHANA_DATA[region]["capital"]
region_pop = GHANA_DATA[region]["pop"]
st.sidebar.info("Region: " + region + " | Capital: " + capital + " | Pop: " + str(region_pop))
st.sidebar.write("District: " + district)
st.sidebar.markdown("---")
st.sidebar.write("AI Planner Ghana - By Emmanuel Gyasi")

st.title("AI Planner Ghana")
st.caption("Plan Smart, Achieve More | " + district + ", " + region + " Region | Built by Emmanuel Gyasi, KNUST")

# ---------- AI BRAIN - RULE BASED, WORKS WITHOUT KEY ----------
def ai_brain(message, region, district):
    msg = message.lower()
    if "exam" in msg or "test" in msg or "mid-sem" in msg:
        return "EXAM PLAN for " + district + ", " + region + ":\n\n1. Today: List all topics. Do past questions for 2 hours.\n2. Tomorrow: Study your weakest topic first. Use 50 min study, 10 min break.\n3. Day 3: Group study with 2 friends. Teach one topic.\n4. Day before exam: Review notes only. Sleep by 10pm. No all-night.\n\nTip for " + region + ": If you have light issues, download notes early and study in morning. You can do this!"
    if "project" in msg or "brief" in msg or "planning" in msg:
        return "PROJECT PLAN for " + district + ":\n\nTitle: Redevelopment / Planning Project in " + district + "\n\nStep 1: Problem - What is wrong in " + district + "? Traffic, drainage, market?\nStep 2: Site Visit - Take 20 photos, talk to 10 people in " + district + ".\nStep 3: Data - Collect population of " + region + " Region, land use, maps.\nStep 4: Proposal - Draw 3 options, pick best one.\nStep 5: Report - Introduction, Problem, Analysis, Proposal, Conclusion.\n\nWant me to generate the full brief? Go to Brief Generator tab and fill it."
    if "timetable" in msg or "schedule" in msg or "time" in msg:
        return "TIMETABLE for " + district + ":\n\n06:00 Wake, pray, review 1 topic\n08:00 Lectures / Classes\n13:00 Lunch + Rest\n15:00 Assignment / Project work (2 hrs)\n18:00 Dinner\n19:30 Study weakest subject (1.5 hrs)\n21:30 Plan tomorrow in AI Planner\n22:30 Sleep\n\nConsistency beats intensity. Follow this 5 days in " + district + " and you will see change."
    if "sample" in msg or "survey" in msg or "population" in msg:
        return "SAMPLING for " + region + " Region:\n\nYour region population is about " + str(region_pop) + ". For a good survey, you need 300-400 people if you want 95% confidence.\n\nDo not survey only " + district + ". Add 2 other towns in " + region + " so your data is not biased.\n\nGo to Sample Calculator tab, enter your population and it will calculate exact sample for you."
    if "career" in msg or "job" in msg or "future" in msg:
        return "CAREER PLAN for " + region + ":\n\nTop jobs in " + region + ": District Planner, GIS Analyst, Real Estate Officer, Environmental Officer.\n\nNext steps:\n1. Learn QGIS (free) - 2 weeks\n2. Learn AutoCAD - 2 weeks\n3. Build 3 projects: Land Use Plan for " + district + ", Map of " + district + ", Brief for " + district + "\n4. Internship: Apply to District Assembly in " + district + ".\n\nYour location is your advantage. People need planners who know " + region + "."
    if "hello" in msg or "hi" in msg or "hey" in msg:
        return "Hello! I am AI Planner Ghana. I know " + district + ", " + region + " Region. Ask me about exams, projects, timetable, sampling, or career. How can I help you today?"
    return "Good question about " + district + "!\n\nHere is a smart plan:\n1. Break it into 3 small steps. Do step 1 today.\n2. Set a deadline. Use Exam Countdown tab.\n3. Study / Work 50 mins, rest 10 mins. Repeat 3 times.\n4. Ask me again with more detail like: 'I have exam in MATH 151 in 5 days in " + district + "' and I will give you a day-by-day plan.\n\nYou are in " + district + ", " + region + " - you can achieve this!"

tab0, tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "Chat with AI Planner",
    "Dashboard",
    "Smart Planner",
    "Sample and Population",
    "Land Use",
    "Brief Generator",
    "Career",
    "Timetable",
    "Exam Countdown"
])

with tab0:
    st.subheader("Chat with AI Planner - Like ChatGPT")
    st.write("You are chatting as a planner in " + district + ", " + region + " Region. Ask anything.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["text"])
    prompt = st.chat_input("Ask me: I have 3 exams next week, plan my week...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "text": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        answer = ai_brain(prompt, region, district)
        st.session_state.chat_history.append({"role": "assistant", "text": answer})
        with st.chat_message("assistant"):
            st.write(answer)
    st.markdown("---")
    st.write("Quick Questions - Click One:")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("Plan my exams"):
        st.session_state.chat_history.append({"role": "user", "text": "Plan my exams"})
        ans = ai_brain("plan my exams", region, district)
        st.session_state.chat_history.append({"role": "assistant", "text": ans})
        st.rerun()
    if c2.button("Plan my project"):
        st.session_state.chat_history.append({"role": "user", "text": "Plan my project"})
        ans = ai_brain("plan my project", region, district)
        st.session_state.chat_history.append({"role": "assistant", "text": ans})
        st.rerun()
    if c3.button("Make timetable"):
        st.session_state.chat_history.append({"role": "user", "text": "Make timetable"})
        ans = ai_brain("make timetable", region, district)
        st.session_state.chat_history.append({"role": "assistant", "text": ans})
        st.rerun()
    if c4.button("Career advice"):
        st.session_state.chat_history.append({"role": "user", "text": "Career advice"})
        ans = ai_brain("career advice", region, district)
        st.session_state.chat_history.append({"role": "assistant", "text": ans})
        st.rerun()

with tab1:
    done = 0
    for t in tasks:
        if t.get("done"):
            done = done + 1
    total = len(tasks)
    pct = 0
    if total > 0:
        pct = int(done / total * 100)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Tasks", total)
    c2.metric("Completed", done)
    c3.metric("Progress", str(pct) + "%")
    st.progress(pct / 100)
    st.info("You are planning from " + district + ", " + region + " Region. Population: " + str(region_pop))
    quotes = [
        "Success is the sum of small efforts repeated day in and day out.",
        "Dont watch the clock, do what it does. Keep going.",
        "Ghana will remember your name if you dont give up.",
        "Plan your work, work your plan."
    ]
    st.info(random.choice(quotes))

with tab2:
    st.subheader("Add New Task - " + district)
    with st.form("task_form", clear_on_submit=True):
        title = st.text_input("Task Title - e.g. Study MATH 151")
        cat = st.selectbox("Category", ["Study", "Assignment", "Project", "Personal", "Exam Prep"])
        due = st.date_input("Due Date", date.today())
        if st.form_submit_button("Add Task"):
            if title:
                tasks.append({"title": title, "cat": cat, "due": str(due), "done": False})
                save("tasks.json", tasks)
                st.success("Task added!")
                st.rerun()
    for i, t in enumerate(tasks):
        col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
        checked = col1.checkbox("", value=t["done"], key="t" + str(i))
        if checked != t["done"]:
            tasks[i]["done"] = checked
            save("tasks.json", tasks)
            st.rerun()
        task_text = t["title"] + " - " + t["cat"] + " | Due: " + t["due"]
        col2.write(task_text)
        if col3.button("Delete", key="d" + str(i)):
            tasks.pop(i)
            save("tasks.json", tasks)
            st.rerun()

with tab3:
    st.subheader("Sample and Population - " + region + " Region")
    st.write("Using Ghana 2021 Census. Your selected region population is pre-filled.")
    pop = st.number_input("Total Population", min_value=10, value=region_pop, step=10)
    margin = st.slider("Margin of Error (%)", 1, 10, 5)
    confidence = st.selectbox("Confidence Level", ["90%", "95%", "99%"])
    if confidence == "90%":
        z = 1.645
    elif confidence == "99%":
        z = 2.576
    else:
        z = 1.96
    p = 0.5
    e = margin / 100
    n0 = (z * z * p * (1 - p)) / (e * e)
    n = math.ceil(n0 / (1 + (n0 - 1) / pop))
    st.metric("Recommended Sample Size", n)
    st.info("From a population of " + str(pop) + " in " + region + ", survey at least " + str(n) + " people. Do not survey only " + district + ". Add other towns to avoid bias.")

with tab4:
    st.subheader("Land Use Planner - " + district)
    total_land = st.number_input("Total Land Area (Hectares) in " + district, min_value=1.0, value=100.0)
    c1, c2, c3, c4 = st.columns(4)
    res = c1.slider("Residential %", 0, 100, 40)
    com = c2.slider("Commercial %", 0, 100, 15)
    green = c3.slider("Green Space %", 0, 100, 20)
    road = c4.slider("Roads %", 0, 100, 15)
    other = 100 - (res + com + green + road)
    st.write("Remaining for Other: " + str(other) + "%")
    if other < 0:
        st.error("Total is over 100%! Reduce one.")
    else:
        df = pd.DataFrame({
            "Use": ["Residential", "Commercial", "Green Space", "Roads", "Other"],
            "Area": [total_land * res / 100, total_land * com / 100, total_land * green / 100, total_land * road / 100, total_land * other / 100]
        })
        st.table(df)
        st.bar_chart(df.set_index("Use"))

with tab5:
    st.subheader("Brief Generator - " + district + ", " + region)
    proj_title = st.text_input("Project Title", "Redevelopment of Market Area in " + district)
    location = st.text_input("Location", district + ", " + region + " Region, Ghana")
    problem = st.text_area("Problem", "Traffic congestion, poor drainage, informal trading blocking access in " + district)
    goal = st.text_area("Goal", "Create a safe, walkable, clean market area in " + district)
    if st.button("Generate Brief"):
        st.markdown("PROJECT BRIEF: " + proj_title)
        st.markdown("Location: " + location)
        st.markdown("Problem: " + problem)
        st.markdown("Objective: " + goal)
        st.markdown("Scope: Site analysis in " + district + ", stakeholder consultation, land use plan, infrastructure proposal.")
        st.markdown("Deliverables: Report, Maps, Site Plan, Presentation.")
        st.markdown("Generated by AI Planner Ghana - Emmanuel Gyasi")

with tab6:
    st.subheader("Career Planner - " + region)
    interest = st.selectbox("What do you love most?", ["Urban Planning", "GIS and Mapping", "Real Estate", "Environmental Planning", "Transport Planning", "Research"])
    if interest == "Urban Planning":
        jobs = ["District Planner at " + district + " Assembly", "Urban Planner at Town and Country Planning", "Consultant at Planning Firm"]
    elif interest == "GIS and Mapping":
        jobs = ["GIS Analyst", "Remote Sensing Specialist", "Mapping Officer"]
    elif interest == "Real Estate":
        jobs = ["Estate Manager", "Valuation Officer", "Property Developer"]
    elif interest == "Environmental Planning":
        jobs = ["Environmental Officer at EPA", "Sustainability Consultant", "Climate Planner"]
    elif interest == "Transport Planning":
        jobs = ["Transport Planner", "Traffic Engineer", "Mobility Consultant"]
    else:
        jobs = ["Teaching Assistant at KNUST", "Research Assistant", "MPhil / PhD in Planning"]
    st.write("Top 3 Careers for " + interest + " in " + region + ":")
    for j in jobs:
        st.write("- " + j)
    st.info("Next Step: Learn QGIS + AutoCAD + Excel. Build 3 projects for " + district + " for your portfolio.")

with tab7:
    st.subheader("My Timetable - " + district)
    with st.form("tt_form", clear_on_submit=True):
        day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        course = st.text_input("Course - e.g. MATH 151")
        start = st.time_input("Start", time(8, 0))
        end = st.time_input("End", time(10, 0))
        venue = st.text_input("Venue - e.g. PB 101")
        if st.form_submit_button("Add To Timetable"):
            if course:
                timetable.append({"day": day, "course": course, "start": str(start), "end": str(end), "venue": venue})
                save("timetable.json", timetable)
                st.rerun()
    if timetable:
        for d in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            dd = []
            for x in timetable:
                if x["day"] == d:
                    dd.append(x)
            if len(dd) > 0:
                st.markdown(d)
                st.table(pd.DataFrame(dd)[["course", "start", "end", "venue"]])

with tab8:
    st.subheader("Exam Countdown")
    with st.form("exam_form", clear_on_submit=True):
        exam_name = st.text_input("Exam - e.g. MATH 151 Mid-Sem")
        exam_date = st.date_input("Exam Date", date.today())
        if st.form_submit_button("Add Exam"):
            if exam_name:
                exams.append({"name": exam_name, "date": str(exam_date)})
                save("exams.json", exams)
                st.rerun()
    today = date.today()
    for i, e in enumerate(exams):
        ed = date.fromisoformat(e["date"])
        days_left = (ed - today).days
        c1, c2, c3 = st.columns([0.5, 0.3, 0.2])
        c1.write(e["name"] + " - " + e["date"])
        if days_left < 0:
            c2.error("Done")
        elif days_left == 0:
            c2.warning("TODAY!")
        elif days_left <= 7:
            c2.warning(str(days_left) + " days left!")
        else:
            c2.success(str(days_left) + " days left")
        if c3.button("Delete", key="ex" + str(i)):
            exams.pop(i)
            save("exams.json", exams)
            st.rerun()