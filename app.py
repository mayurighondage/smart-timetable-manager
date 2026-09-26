import streamlit as st
import pandas as pd

# Page Config
st.set_page_config(
    page_title="EduNova AI - Smart Timetable Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED EDUNOVA-STYLE CSS STYLING ---
st.markdown("""
    <style>
    /* Global Page Styling */
    .stApp {
        background-color: #f3f6fb !important;
        color: #1e293b;
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    /* Left Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }

    /* Top Welcome Hero Banner */
    .hero-card {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-radius: 20px;
        padding: 24px 30px;
        border: 1px solid #bae6fd;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .hero-title {
        color: #0369a1;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
    }
    .hero-subtitle {
        color: #0284c7;
        font-size: 0.95rem;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Metric Cards */
    .edu-card {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 18px 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        margin-bottom: 15px;
    }
    .edu-card-title {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    .edu-card-val {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0f172a;
        margin: 4px 0;
    }

    /* Timeline Slot Badges */
    .slot-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 12px 16px;
        border-left: 4px solid #0284c7;
        margin-bottom: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .slot-time {
        font-size: 0.75rem;
        font-weight: 700;
        color: #0284c7;
    }
    .slot-title {
        font-size: 0.9rem;
        font-weight: 700;
        color: #0f172a;
        margin: 2px 0;
    }
    .slot-room {
        font-size: 0.8rem;
        color: #64748b;
    }

    /* Primary Buttons */
    .stButton>button {
        background-color: #0284c7 !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
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


# ==============================================================================
# MODULE 1: TEACHER DASHBOARD (EDUNOVA LOOK)
# ==============================================================================
if choice == "🏠 Teacher Dashboard":
    
    # 2 Main Section Layout (Center Main Dashboard + Right Side Schedule Panel)
    center_col, right_col = st.columns([2.8, 1.2])
    
    with center_col:
        # Personalized Greeting Hero Banner
        st.markdown("""
            <div class="hero-card">
                <div>
                    <div class="hero-title">Good morning, Dr. Sharma! 👋</div>
                    <div class="hero-subtitle">Empower minds. Inspire futures. You have 3 lectures scheduled today and 1 substitute request.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 4 Metric Cards Row
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.markdown("""
            <div class="edu-card">
                <div class="edu-card-title">Today's Lectures</div>
                <div class="edu-card-val">3</div>
                <small style="color:#0284c7;">Next: ML at 09:00 AM</small>
            </div>
            """, unsafe_allow_html=True)
            
        with mc2:
            st.markdown("""
            <div class="edu-card">
                <div class="edu-card-title">Free Slot Hours</div>
                <div class="edu-card-val">2</div>
                <small style="color:#16a34a;">Available for office hours</small>
            </div>
            """, unsafe_allow_html=True)
            
        with mc3:
            st.markdown("""
            <div class="edu-card">
                <div class="edu-card-title">Weekly Load</div>
                <div class="edu-card-val">14 <span style="font-size:1rem;">/16h</span></div>
                <small style="color:#d97706;">87% Capacity</small>
            </div>
            """, unsafe_allow_html=True)
            
        with mc4:
            st.markdown("""
            <div class="edu-card">
                <div class="edu-card-title">Pending Substitutes</div>
                <div class="edu-card-val">1</div>
                <small style="color:#dc2626;">Requires Action</small>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("### ⚡ Quick Navigation Links")
        q1, q2, q3, q4 = st.columns(4)
        q1.button("📅 View Timetable")
        q2.button("⚡ Request Substitute")
        q3.button("🏫 Room Tracker")
        q4.button("📈 Progress Report")

        st.write("")
        st.markdown("### 📊 Departmental Teaching Performance & Syllabus")
        
        perf_df = pd.DataFrame([
            {"Subject Module": "Machine Learning (TY AI&DS)", "Assigned Faculty": "Dr. Sharma", "Completed Topics": "16 / 20", "Progress": "80%"},
            {"Subject Module": "Database Management (SY AI&DS)", "Assigned Faculty": "Prof. Patil", "Completed Topics": "10 / 20", "Progress": "50%"},
            {"Subject Module": "Data Structures (SY Comp)", "Assigned Faculty": "Dr. Kulkarni", "Completed Topics": "14 / 20", "Progress": "70%"},
            {"Subject Module": "Advanced AI (B.Tech AI&DS)", "Assigned Faculty": "Prof. Joshi", "Completed Topics": "18 / 20", "Progress": "90%"},
        ])
        st.dataframe(perf_df, use_container_width=True, hide_index=True)

    # Right Sidebar Column (Calendar + Daily Schedule Timeline)
    with right_col:
        st.markdown("### 📅 Calendar Overview")
        st.caption("September 2026")
        
        st.markdown("#### Today's Schedule Timeline")
        
        st.markdown("""
        <div class="slot-card">
            <div class="slot-time">09:00 AM - 10:00 AM</div>
            <div class="slot-title">Class 10A - Machine Learning</div>
            <div class="slot-room">📍 Room 101 • TY AI&DS</div>
        </div>
        
        <div class="slot-card" style="border-left-color: #eab308;">
            <div class="slot-time">10:00 AM - 11:00 AM</div>
            <div class="slot-title">Free Slot / Research Hour</div>
            <div class="slot-room">📍 Faculty Cabin 3</div>
        </div>
        
        <div class="slot-card">
            <div class="slot-time">11:15 AM - 01:15 PM</div>
            <div class="slot-title">Class 11B - ML Lab Practical</div>
            <div class="slot-room">📍 Lab 201 (AI Lab) • Batch B1</div>
        </div>
        
        <div class="slot-card" style="border-left-color: #16a34a;">
            <div class="slot-time">02:00 PM - 03:00 PM</div>
            <div class="slot-title">Class 12A - Advanced AI</div>
            <div class="slot-room">📍 Room 102 • SY AI&DS</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.markdown("#### 🔔 Smart Reminders")
        st.info("⏰ **Upcoming Lecture:** ML in 15 mins (Room 101)")
        st.warning("📋 **Substitute Alert:** Prof. Patil requested cover for 02:00 PM slot")


# ==============================================================================
# MODULE 2: MASTER TIMETABLE
# ==============================================================================
elif choice == "📋 Master Timetable":
    st.title("📋 Master Timetable & Clash Detector")
    
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1:
        st.selectbox("Filter Day:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    with c2:
        st.selectbox("Filter Class:", ["SY AI&DS", "TY AI&DS", "B.Tech AI&DS"])
    with c3:
        st.text_input("🔍 Search Subject / Teacher / Room:")
        
    st.success("✅ Zero schedule conflicts detected across all active slots.")
    
    master_df = pd.DataFrame([
        {"Time Slot": "09:00 - 10:00 AM", "Subject": "Machine Learning", "Faculty": "Dr. Sharma", "Room": "Room 101", "Status": "PASS"},
        {"Time Slot": "10:00 - 11:00 AM", "Subject": "Database Systems", "Faculty": "Prof. Patil", "Room": "Room 102", "Status": "PASS"},
        {"Time Slot": "11:15 - 12:15 PM", "Subject": "Data Structures", "Faculty": "Dr. Kulkarni", "Room": "Room 101", "Status": "PASS"},
        {"Time Slot": "12:15 - 01:15 PM", "Subject": "AI & Robotics", "Faculty": "Prof. Joshi", "Room": "Lab 202", "Status": "PASS"},
    ])
    st.dataframe(master_df, use_container_width=True, hide_index=True)


# ==============================================================================
# MODULE 3: AI SUBSTITUTE RECOMMENDATION
# ==============================================================================
elif choice == "⚡ AI Substitute Recommendation":
    st.title("⚡ AI Substitute Recommendation Engine")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Report Absence")
        st.selectbox("Select Absent Teacher:", ["Dr. Sharma (ML)", "Prof. Patil (DBMS)"])
        st.selectbox("Affected Slot:", ["09:00 AM - 10:00 AM"])
        st.text_area("Reason:", "Sick Leave")
        if st.button("Find Best Substitutes"):
            st.success("Recommendation generated!")
            
    with col2:
        st.subheader("2. System Recommendations")
        st.success("🥇 **Prof. Joshi** (Suitability: 96% | Load: 8 hrs)")
        st.warning("🥈 **Dr. Kulkarni** (Suitability: 82% | Load: 11 hrs)")


# ==============================================================================
# MODULE 4: INFRASTRUCTURE ROOM TRACKER
# ==============================================================================
elif choice == "🏫 Infrastructure Room Tracker":
    st.title("🏫 Live Room & Lab Occupancy Status")
    
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Room 101", "Occupied", "TY AI&DS")
    r2.metric("Room 102", "Vacant", "Available")
    r3.metric("Lab 201 (AI)", "Occupied", "SY AI&DS")
    r4.metric("Lab 202 (DS)", "Vacant", "Available")


# ==============================================================================
# MODULE 5: SYLLABUS & WORKLOAD ANALYTICS
# ==============================================================================
elif choice == "📊 Syllabus & Workload Analytics":
    st.title("📊 Workload & Progress Analytics")
    
    st.write("### Faculty Workload Breakdown")
    st.progress(14 / 16, text="Dr. Sharma (14/16 Hours)")
    st.progress(12 / 16, text="Prof. Patil (12/16 Hours)")
    st.progress(8 / 16, text="Prof. Joshi (8/16 Hours)")