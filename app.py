import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Hospital Wait Time System",
    layout="wide",
    page_icon="🏥"
)

# ================= LOGIN SESSION STATE =================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# ================= MODERN CSS THEME =================
st.markdown("""
<style>
.stApp {
    background-color: #F8FAFC;
    font-family: 'Segoe UI', sans-serif;
}
section[data-testid="stSidebar"] {
    background-color: #1E2A38;
}
section[data-testid="stSidebar"] * {
    color: #ECF0F1;
}
.metric-card {
    background: #E6FFFA;
    border-radius: 16px;
    padding: 22px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
.stButton>button {
    background: linear-gradient(90deg, #16A085, #1ABC9C);
    color: white;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ================= MODERN LOGIN PAGE =================
def login_page():

    # ---------- Top card ----------
    st.markdown("""
    <style>
    .login-card {
        background: white;
        padding: 35px 40px;
        border-radius: 18px;
        width: 360px;
        margin: 60px auto 25px auto;
        box-shadow: 0 20px 45px rgba(0,0,0,0.12);
        text-align: center;
    }
    .login-title {
        font-size: 22px;
        font-weight: 700;
        color: #1E2A38;
        margin-bottom: 6px;
    }
    .login-subtitle {
        font-size: 14px;
        color: #6B7280;
    }
    </style>

    <div class="login-card">
        <div class="login-title">🏥 Hospital Wait Time System</div>
        <div class="login-subtitle">
            Smart AI-based Queue Prediction
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---------- Centered login controls ----------
    left, center, right = st.columns([1, 2, 1])

    with center:
        role = st.radio(
            "Login as",
            ["User", "Admin"],
            horizontal=True,
            key="login_role"
        )

        username = st.text_input(
            "Username",
            placeholder="Enter username",
            key="login_user"
        )

        if role == "Admin":
            password = st.text_input(
                "Admin PIN",
                type="password",
                placeholder="Enter admin PIN",
                key="login_pin"
            )

        if st.button("Login", use_container_width=True):
            if role == "User" and username:
                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.rerun()

            elif role == "Admin" and username and password == "1234":
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.rerun()

            else:
                st.error("❌ Invalid credentials")


# ================= LOGIN GATE =================
if not st.session_state.logged_in:
    login_page()
    st.stop()

# ================= LOAD MODEL =================
model = joblib.load("hospital_wait_model.pkl")
residual_std = joblib.load("residual_std.pkl")

# ================= HEADER =================
st.markdown("""
<div style="
    background: linear-gradient(90deg, #1E2A38, #16A085);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 30px;
">
    <h1 style="text-align:center; color:white;">
        Hospital Wait Time Prediction System
    </h1>
    <p style="text-align:center; color:#DFF9FB; font-size:22px;">
        AI-based Patient Prediction & Hospital Decision Support
    </p>
</div>
""", unsafe_allow_html=True)

# ================= LOGOUT =================
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.role = None
    st.rerun()

# ================= ROLE-BASED TABS =================
if st.session_state.role == "user":
    user_tab, = st.tabs(["👤 User Mode"])
else:
    user_tab, admin_tab = st.tabs(["👤 User Mode", "🛠️ Admin Mode"])

# ================= DEFAULT VALUES =================
DEFAULT_DOCTORS = 3
DEFAULT_EXPERIENCE = 8
AVG_CONSULT_TIME = 12

# ================= METRIC CARD =================
def metric_card(title, value, icon):
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size:28px;">{icon}</div>
        <div style="color:#1E2A38; font-size:16px; font-weight:600;">
            {title}
        </div>
        <div style="color:#16A085; font-size:34px; font-weight:800;">
            {value}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ================= USER MODE =================
with user_tab:
    st.subheader("👤 Patient Wait Time Prediction")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Patient Age", 1, 90, 35, key="user_age")
        urgency = st.selectbox(
            "Urgency Level",
            [0, 1, 2],
            format_func=lambda x: ["Normal", "Urgent", "Emergency"][x],
            key="user_urgency"
        )
        visit_type = st.selectbox(
            "Visit Type",
            [0, 1, 2],
            format_func=lambda x: ["Walk-in", "Appointment", "Follow-up"][x],
            key="user_visit"
        )

    with col2:
        arrival_slot = st.selectbox(
            "Arrival Slot",
            [0, 1, 2],
            format_func=lambda x: ["Morning", "Afternoon", "Evening"][x],
            key="user_arrival"
        )
        patients_in_queue = st.slider(
            "Estimated Patients in Queue",
            0, 50, 10,
            key="user_patients"
        )
        is_peak = st.selectbox(
            "Peak Hour?",
            [0, 1],
            format_func=lambda x: ["No", "Yes"][x],
            key="user_peak"
        )

    if st.button("🔮 Predict Wait Time", key="user_predict"):

        is_elderly = 1 if age >= 60 else 0
        priority_score = urgency * 3 + is_elderly * 2 + (1 if visit_type == 2 else 0)
        doctor_utilization = patients_in_queue / DEFAULT_DOCTORS

        input_df = pd.DataFrame([{
            "age": age,
            "urgency_level": urgency,
            "visit_type": visit_type,
            "arrival_slot": arrival_slot,
            "patients_in_queue": patients_in_queue,
            "avg_consult_time": AVG_CONSULT_TIME,
            "doctors_available": DEFAULT_DOCTORS,
            "doctor_experience_avg": DEFAULT_EXPERIENCE,
            "is_peak_hour": is_peak,
            "doctor_utilization": doctor_utilization,
            "priority_score": priority_score
        }])

        expected = model.predict(input_df)[0]
        min_w = max(0, expected - residual_std)
        max_w = expected + residual_std

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Expected Wait (min)", f"{expected:.1f}", "⏱️")
        with c2:
            metric_card("Minimum Wait", f"{min_w:.1f}", "⬇️")
        with c3:
            metric_card("Maximum Wait", f"{max_w:.1f}", "⬆️")

        st.markdown("### 📊 Visual Insights")

        g1, g2 = st.columns(2)

        with g1:
            wait_df = pd.DataFrame({
                "Type": ["Minimum", "Expected", "Maximum"],
                "Wait Time (minutes)": [min_w, expected, max_w],
                "Meaning": [
                    "Best case scenario",
                    "Most likely waiting time",
                    "Worst case scenario"
                ]
            })

            fig_wait = px.bar(
                wait_df,
                x="Type",
                y="Wait Time (minutes)",
                hover_data=["Meaning"],
                title="⏱️ Waiting Time Range",
                color="Type",
                color_discrete_sequence=["#6EE7B7", "#34D399", "#059669"]
            )
            fig_wait.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_wait, use_container_width=True)

        with g2:
            load_df = pd.DataFrame({
                "Category": ["Patients Waiting", "Doctors Available"],
                "Count": [patients_in_queue, DEFAULT_DOCTORS],
                "Explanation": [
                    "Patients currently in queue",
                    "Doctors currently available"
                ]
            })

            fig_load = px.bar(
                load_df,
                x="Category",
                y="Count",
                hover_data=["Explanation"],
                title="👨‍⚕️ Hospital Load",
                color="Category",
                color_discrete_sequence=["#FBBF24", "#60A5FA"]
            )
            fig_load.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig_load, use_container_width=True)

# ================= ADMIN MODE =================
if st.session_state.role == "admin":
    with admin_tab:
        st.subheader("🛠️ Hospital Admin Decision Panel")

        c1, c2, c3 = st.columns(3)
        patients = c1.slider("Patients in Queue", 0, 60, 25, key="admin_patients")
        doctors = c2.slider("Doctors On Duty", 1, 10, DEFAULT_DOCTORS, key="admin_doctors")
        peak = c3.selectbox(
            "Peak Hour?",
            [0, 1],
            format_func=lambda x: ["No", "Yes"][x],
            key="admin_peak"
        )

        urgency_admin = st.selectbox(
            "Dominant Urgency Level",
            [0, 1, 2],
            format_func=lambda x: ["Normal", "Urgent", "Emergency"][x],
            key="admin_urgency"
        )

        if st.button("📊 Analyze & Decide", key="admin_analyze"):
            utilization = patients / doctors
            priority_score = urgency_admin * 3

            admin_df = pd.DataFrame([{
                "age": 45,
                "urgency_level": urgency_admin,
                "visit_type": 0,
                "arrival_slot": 1,
                "patients_in_queue": patients,
                "avg_consult_time": AVG_CONSULT_TIME,
                "doctors_available": doctors,
                "doctor_experience_avg": DEFAULT_EXPERIENCE,
                "is_peak_hour": peak,
                "doctor_utilization": utilization,
                "priority_score": priority_score
            }])

            current_wait = model.predict(admin_df)[0]

            admin_df["doctors_available"] += 1
            admin_df["doctor_utilization"] = patients / (doctors + 1)
            new_wait = model.predict(admin_df)[0]

            c1, c2 = st.columns(2)
            with c1:
                metric_card("Current Wait", f"{current_wait:.1f}", "⏱️")
            with c2:
                metric_card("With +1 Doctor", f"{new_wait:.1f}", "➕")

            if current_wait - new_wait > 15:
                st.error("🚨 Recommendation: ADD A DOCTOR NOW")
            else:
                st.success("✅ Current staffing is sufficient")
