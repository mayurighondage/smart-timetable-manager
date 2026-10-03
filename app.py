import streamlit as st
import pandas as pd

# Safe import for Plotly
try:
    import plotly.graph_objects as go
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

# Page Config
st.set_page_config(
    page_title="EduNova AI - Smart Timetable Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INITIALIZE SESSION STATE ---
if "substitute_requests" not in st.session_state:
    st.session_state.substitute_requests = [
        {
            "id": 101,
            "requester": "Prof. Patil",
            "subject": "DBMS (SY AI&DS)",
            "slot": "02:00 PM - 03:00 PM",
            "recommended": "Dr. Sharma",
            "reason": "Health Emergency",
            "status": "Pending"
        }
    ]

# --- FACULTY DATABASE ---
FACULTY_DATA = [
    {"name": "Dr. Kulkarni", "expertise": ["Machine Learning", "AI", "Data Structures"], "load": "10/16h", "availability": "Free at 09:00 AM & 02:00 PM"},
    {"name": "Prof. Joshi", "expertise": ["DBMS", "Python", "SQL"], "load": "8/16h", "availability": "Free at 09:00 AM & 11:15 AM"},
    {"name": "Prof. Pawar", "expertise": ["Computer Networks", "DBMS"], "load": "12/16h", "availability": "Free at 02:00 PM"},
    {"name": "Dr. Sharma", "expertise": ["Machine Learning", "Advanced AI"], "load": "14/16h", "availability": "Free at 10:00 AM"}
]

# --- FACULTY PERSONAL DATA ---
FACULTY_PERSONAL_DATA = {
    "Dr. Sharma": {
        "hours": 14,
        "max_hours": 16,
        "classes": [
            {"subject": "Machine Learning", "class": "TY AI&DS", "units": "4 / 6", "progress": 66, "status": "On Track"},
            {"subject": "Advanced AI Topics", "class": "B.Tech AI&DS", "units": "5 / 6", "progress": 83, "status": "Ahead"},
            {"subject": "ML Lab Practical", "class": "TY AI&DS (Batch B1)", "units": "8 / 10 Labs", "progress": 80, "status": "Ahead"}
        ]
    },
    "Prof. Patil": {
        "hours": 12,
        "max_hours": 16,
        "classes": [
            {"subject": "Database Management (DBMS)", "class": "SY AI&DS", "units": "5 / 6", "progress": 83, "status": "Ahead"},
            {"subject": "DBMS Lab", "class": "SY AI&DS (Batch A)", "units": "6 / 10 Labs", "progress": 60, "status": "On Track"}
        ]
    },
    "Prof. Joshi": {
        "hours": 8,
        "max_hours": 16,
        "classes": [
            {"subject": "Python Programming", "class": "FY AI&DS", "units": "3 / 6", "progress": 50, "status": "On Track"},
            {"subject": "Data Structures & Algo", "class": "SY AI&DS", "units": "2 / 6", "progress": 33, "status": "Behind Schedule"}
        ]
    },
    "Dr. Kulkarni": {
        "hours": 10,
        "max_hours": 16,
        "classes": [
            {"subject": "Data Mining", "class": "TY AI&DS", "units": "4 / 6", "progress": 66, "status": "On Track"}
        ]
    },
    "Prof. Pawar": {
        "hours": 12,
        "max_hours": 16,
        "classes": [
            {"subject": "Computer Networks", "class": "SY AI&DS", "units": "2 / 6", "progress": 33, "status": "Behind Schedule"}
        ]
    }
}

# --- CSS STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f3f6fb !important;
        color: #1e293b;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    .block-container {
        padding-top: 1.8rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Custom Radio Button Accent Styling */
    div[data-testid="stRadio"] label p {
        font-size: 0.98rem !important;
        font-weight: 500 !important;
        color: #0369a1 !important;
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] input[type="radio"]:checked + div {
        background-color: #ff4b4b !important;
        border-color: #ff4b4b !important;
    }

    /* Cards */
    .hero-card {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-radius: 18px;
        padding: 24px 32px;
        border: 1px solid #bae6fd;
        margin-bottom: 20px;
    }
    .hero-title {
        color: #0369a1;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    .hero-subtitle {
        color: #0284c7;
        font-size: 1rem;
        margin-top: 6px;
        font-weight: 500;
    }

    .edu-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px 22px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 15px;
    }
    .edu-card-title {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 700;
        text-transform: uppercase;
    }
    .edu-card-val {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0f172a;
        margin: 4px 0;
    }

    .timeline-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }
    .slot-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 14px 18px;
        border-left: 5px solid #0284c7;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .slot-time {
        font-size: 0.78rem;
        font-weight: 700;
        color: #0284c7;
    }
    .slot-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #0f172a;
        margin: 3px 0;
    }

    .upcoming-box {
        background-color: #e0f2fe;
        border: 1px solid #bae6fd;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 15px;
    }

    .substitute-box {
        background-color: #fef9c3;
        border: 1px solid #fef08a;
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }

    .ai-card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 5px solid #0284c7;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("### 🎓 **EduNova AI** ERP")
st.sidebar.caption("Smart Timetable & Departmental AI Manager")
st.sidebar.divider()

menu = [
    "🏠 Teacher Dashboard",
    "📋 Master Timetable",
    "⚡ AI Substitute Recommendation",
    "🏫 Infrastructure Room Tracker",
    "📊 Syllabus & Workload Analytics"
]

choice = st.sidebar.radio("Navigation Menu:", menu)

st.sidebar.divider()
st.sidebar.info("💡 **Active Semester:** Autumn 2026\n\n**Department:** AI & Data Science")

# --- PAGE 1: TEACHER DASHBOARD ---
if choice == "🏠 Teacher Dashboard":
    st.markdown("""
        <div class="hero-card">
            <div class="hero-title">Good morning, Dr. Sharma! 👋</div>
            <div class="hero-subtitle">Empower minds. Inspire futures. You have 3 lectures scheduled today and 1 substitute request.</div>
        </div>
    """, unsafe_allow_html=True)
    
    pending_requests = [r for r in st.session_state.substitute_requests if r['status'] == 'Pending']
    pending_count = len(pending_requests)

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown("""
        <div class="edu-card">
            <div class="edu-card-title">Today's Lectures</div>
            <div class="edu-card-val">3</div>
            <small style="color:#0284c7; font-weight:600;">Next: ML at 09:00 AM</small>
        </div>
        """, unsafe_allow_html=True)
        
    with mc2:
        st.markdown("""
        <div class="edu-card">
            <div class="edu-card-title">Free Slot Hours</div>
            <div class="edu-card-val">2</div>
            <small style="color:#16a34a; font-weight:600;">Available for office hours</small>
        </div>
        """, unsafe_allow_html=True)
        
    with mc3:
        st.markdown("""
        <div class="edu-card">
            <div class="edu-card-title">Weekly Load</div>
            <div class="edu-card-val">14 <span style="font-size:1.1rem; color:#64748b;">/16h</span></div>
            <small style="color:#d97706; font-weight:600;">87% Capacity</small>
        </div>
        """, unsafe_allow_html=True)
        
    with mc4:
        st.markdown(f"""
        <div class="edu-card">
            <div class="edu-card-title">Pending Substitutes</div>
            <div class="edu-card-val">{pending_count}</div>
            <small style="color:#dc2626; font-weight:600;">Requires Action</small>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.markdown("### ⚡ Quick System Actions")
    q1, q2, q3, q4 = st.columns(4)
    q1.button("📅 View Timetable")
    q2.button("⚡ Request Substitute")
    q3.button("🏫 Room Tracker")
    q4.button("📈 Progress Report")

    st.write("")
    st.divider()

    t_col1, t_col2 = st.columns([2, 1], gap="large")

    with t_col1:
        st.markdown("### 📅 Today's Timeline")
        st.write("")
        st.markdown("""
        <div class="timeline-container">
            <div class="slot-card">
                <div class="slot-time">09:00 AM - 10:00 AM</div>
                <div class="slot-title">Class 10A - Machine Learning</div>
                <div style="font-size:0.82rem; color:#64748b;">📍 Room 101 • TY AI&DS</div>
            </div>
            <div class="slot-card" style="border-left-color: #eab308;">
                <div class="slot-time">10:00 AM - 11:00 AM</div>
                <div class="slot-title">Free Slot / Research Hour</div>
                <div style="font-size:0.82rem; color:#64748b;">📍 Faculty Cabin 3</div>
            </div>
            <div class="slot-card">
                <div class="slot-time">11:15 AM - 01:15 PM</div>
                <div class="slot-title">Class 11B - ML Lab Practical</div>
                <div style="font-size:0.82rem; color:#64748b;">📍 Lab 201 (AI Lab) • Batch B1</div>
            </div>
            <div class="slot-card" style="border-left-color: #16a34a;">
                <div class="slot-time">02:00 PM - 03:00 PM</div>
                <div class="slot-title">Class 12A - Advanced AI</div>
                <div style="font-size:0.82rem; color:#64748b;">📍 Room 102 • SY AI&DS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with t_col2:
        st.markdown("### 🔔 System Notifications")
        st.write("")
        st.markdown("""
            <div class="upcoming-box">
                <div style="font-size:0.95rem; font-weight:700; color:#0369a1;">⏰ Upcoming Lecture</div>
                <div style="margin-top:6px; font-size:0.88rem; color:#0f172a;">
                    <strong>Machine Learning (TY AI&DS)</strong><br>
                    <span style="color:#0284c7; font-weight:600;">Starts in 15 mins</span> (09:00 AM)<br>
                    📍 Room 101 • Main Academic Building
                </div>
            </div>
        """, unsafe_allow_html=True)

        if pending_count > 0:
            st.markdown("#### 📋 Substitute Actions")
            for req in pending_requests:
                st.markdown(f"""
                    <div class="substitute-box">
                        <div style="font-size:0.95rem; font-weight:700; color:#854d0e;">📋 Cover Request From {req['requester']}</div>
                        <div style="font-size:0.85rem; color:#475569; margin-top:6px;">
                            <strong>Subject:</strong> {req['subject']}<br>
                            <strong>Slot:</strong> {req['slot']}<br>
                            <strong>Reason:</strong> {req['reason']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                btn1, btn2 = st.columns(2)
                with btn1:
                    if st.button("✅ Accept", key=f"dash_acc_{req['id']}", use_container_width=True):
                        req["status"] = "Accepted"
                        st.success("Accepted substitute request!")
                        st.rerun()
                with btn2:
                    if st.button("❌ Reject", key=f"dash_rej_{req['id']}", use_container_width=True):
                        req["status"] = "Rejected"
                        st.error("Rejected substitute request!")
                        st.rerun()
        else:
            st.success("🎉 No pending substitute requests!")

# --- PAGE 2: MASTER TIMETABLE ---
elif choice == "📋 Master Timetable":
    st.title("📋 Master Timetable")
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1: st.selectbox("Filter Day:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    with c2: st.selectbox("Filter Class:", ["SY AI&DS", "TY AI&DS", "B.Tech AI&DS"])
    with c3: st.text_input("🔍 Search Subject / Teacher / Room:")
    st.success("✅ Zero schedule conflicts detected across all active slots.")

# --- PAGE 3: AI SUBSTITUTE RECOMMENDATION ---
elif choice == "⚡ AI Substitute Recommendation":
    st.title("⚡ AI-Powered Substitute Recommendation Engine")
    st.caption("AI analyzes free slots, workload capacity, and domain relevance to suggest optimal substitutes.")
    
    col1, col2 = st.columns([1.2, 1.8], gap="large")
    
    with col1:
        st.markdown("### 🔍 Select Class Details")
        requester = st.selectbox("Absent Teacher:", ["Dr. Sharma", "Prof. Patil", "Dr. Kulkarni"])
        subject = st.selectbox("Subject to Cover:", ["Machine Learning", "DBMS", "Data Structures", "Python"])
        slot = st.selectbox("Time Slot:", ["09:00 AM - 10:00 AM", "11:15 AM - 12:15 PM", "02:00 PM - 03:00 PM"])
        reason = st.text_area("Reason for Absence:", placeholder="e.g., Medical Emergency")
        
        st.button("⚡ Find AI Recommendations", use_container_width=True, type="primary")

    with col2:
        st.markdown("### 🤖 Recommended Substitutes")
        recommendations = []
        for fac in FACULTY_DATA:
            if fac["name"] != requester:
                score = 50
                if subject in fac["expertise"]:
                    score += 35
                if slot.split(" - ")[0] in fac["availability"]:
                    score += 15
                
                recommendations.append({
                    "name": fac["name"],
                    "match_score": score,
                    "load": fac["load"],
                    "expertise": ", ".join(fac["expertise"]),
                    "status": "Available" if slot.split(" - ")[0] in fac["availability"] else "Busy"
                })
        
        recommendations = sorted(recommendations, key=lambda x: x["match_score"], reverse=True)
        
        for idx, rec in enumerate(recommendations):
            badge_color = "#16a34a" if rec["match_score"] >= 80 else ("#eab308" if rec["match_score"] >= 60 else "#dc2626")
            
            st.markdown(f"""
                <div class="ai-card">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <strong style="font-size:1.05rem; color:#0f172a;">{rec['name']}</strong>
                        <span style="background-color:{badge_color}; color:white; padding:3px 10px; border-radius:12px; font-size:0.8rem; font-weight:700;">
                            {rec['match_score']}% AI Match
                        </span>
                    </div>
                    <div style="font-size:0.85rem; color:#64748b; margin-top:6px;">
                        📚 <strong>Expertise:</strong> {rec['expertise']} <br>
                        ⚖️ <strong>Current Workload:</strong> {rec['load']} | 🟢 <strong>Slot Status:</strong> {rec['status']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"📩 Request {rec['name']}", key=f"rec_btn_{idx}"):
                st.session_state.substitute_requests.append({
                    "id": len(st.session_state.substitute_requests) + 101,
                    "requester": requester,
                    "subject": f"{subject} ({slot})",
                    "slot": slot,
                    "recommended": rec['name'],
                    "reason": reason if reason else "Not Specified",
                    "status": "Pending"
                })
                st.success(f"✅ Substitute request sent to {rec['name']}!")
                st.rerun()

# --- PAGE 4: INFRASTRUCTURE ROOM TRACKER ---
elif choice == "🏫 Infrastructure Room Tracker":
    st.title("🏫 Live Room & Lab Occupancy Status")
    st.write("Live status of classroom and lab availability.")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Room 101", "Occupied", "TY AI&DS")
    r2.metric("Room 102", "Vacant", "Available")
    r3.metric("Lab 201 (AI)", "Occupied", "SY AI&DS")
    r4.metric("Lab 202 (DS)", "Vacant", "Available")

# --- PAGE 5: SYLLABUS & WORKLOAD ANALYTICS ---
elif choice == "📊 Syllabus & Workload Analytics":
    st.markdown("""
        <div class="hero-card" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-color: #bae6fd;">
            <div class="hero-title" style="color: #0369a1;">📊 My Workload & Syllabus Analytics</div>
            <div class="hero-subtitle" style="color: #0284c7;">Personalized faculty workload gauge chart and syllabus progress across assigned classes.</div>
        </div>
    """, unsafe_allow_html=True)

    col_sel1, col_sel2 = st.columns([1.5, 2.5])
    with col_sel1:
        current_faculty = st.selectbox(
            "👤 Select Faculty Account:",
            list(FACULTY_PERSONAL_DATA.keys()),
            index=0
        )

    fac_data = FACULTY_PERSONAL_DATA.get(current_faculty, FACULTY_PERSONAL_DATA["Dr. Sharma"])
    hours_logged = fac_data["hours"]
    max_hours = fac_data["max_hours"]
    workload_pct = int((hours_logged / max_hours) * 100)

    st.write("")
    st.divider()

    col_chart, col_classes = st.columns([1, 2], gap="large")

    with col_chart:
        st.markdown(f"### ⚖️ Workload Capacity")
        st.caption(f"Weekly assigned hours against maximum cap ({max_hours} Hours).")

        if HAS_PLOTLY:
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=workload_pct,
                number={'suffix': "%", 'font': {'size': 36, 'color': '#0f172a'}},
                title={'text': f"<b>{hours_logged} / {max_hours} Hours</b>", 'font': {'size': 13, 'color': '#64748b'}},
                gauge={
                    'axis': {'range': [0, 100], 'visible': False},
                    'bar': {'color': "#0284c7", 'thickness': 0.75},
                    'bgcolor': "#f1f5f9",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 50], 'color': '#e0f2fe'},
                        {'range': [50, 85], 'color': '#bae6fd'},
                        {'range': [85, 100], 'color': '#fef08a'}
                    ],
                    'threshold': {
                        'line': {'color': "#dc2626", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))

            fig.update_layout(
                margin=dict(l=10, r=10, t=20, b=0),
                height=200,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ `plotly` package not found. Install via `pip install plotly` for gauge visuals.")
            st.progress(workload_pct / 100)

    with col_classes:
        st.markdown(f"### 📚 Class Syllabus Progress")
        st.caption("Live completion status across all assigned classes.")
        st.write("")

        if HAS_PLOTLY:
            # Side-by-side columns for each class's gauge meter
            class_cols = st.columns(len(fac_data["classes"]))
            
            for idx, cls in enumerate(fac_data["classes"]):
                with class_cols[idx]:
                    badge_color = "#16a34a" if cls["status"] == "Ahead" else ("#0284c7" if cls["status"] == "On Track" else "#dc2626")
                    
                    st.markdown(f"""
                    <div class="edu-card" style="padding:12px; text-align:center; margin-bottom: 0px;">
                        <span style="background-color:{badge_color}; color:white; padding:2px 8px; border-radius:10px; font-size:0.75rem; font-weight:700;">
                            {cls['status']}
                        </span>
                        <div style="font-weight:700; color:#0f172a; font-size:0.95rem; margin-top:6px;">{cls['subject']}</div>
                        <div style="font-size:0.78rem; color:#64748b;">📍 {cls['class']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    gauge_fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=cls["progress"],
                        number={'suffix': "%", 'font': {'size': 26, 'color': '#0f172a'}},
                        title={'text': f"Units: {cls['units']}", 'font': {'size': 12, 'color': '#64748b'}},
                        gauge={
                            'axis': {'range': [0, 100], 'visible': False},
                            'bar': {'color': badge_color, 'thickness': 0.75},
                            'bgcolor': "#f1f5f9",
                            'borderwidth': 0,
                            'steps': [
                                {'range': [0, cls["progress"]], 'color': badge_color},
                                {'range': [cls["progress"], 100], 'color': '#e2e8f0'}
                            ]
                        }
                    ))

                    gauge_fig.update_layout(
                        margin=dict(l=10, r=10, t=20, b=0),
                        height=160,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)"
                    )
                    st.plotly_chart(gauge_fig, use_container_width=True)
        else:
            for cls in fac_data["classes"]:
                st.write(f"**{cls['subject']} ({cls['class']}):** {cls['progress']}%")
                st.progress(cls["progress"] / 100)
