
import streamlit as st
import sys
from pathlib import Path
# Import database functions
sys.path.append(str(Path(__file__).resolve().parent.parent))
from database.db import create_tables, save_learner
# Configure the page
st.set_page_config(
    page_title="Learner Setup",
    page_icon="👩‍🎓",
    layout="wide"
)


# Learner Setup page styling
st.markdown("""
<style>

/* Page heading */
h1 {
    font-size: 36px !important;
    font-weight: 800 !important;
    color: #5836A3 !important;
}

/* Section headings */
h2, h3 {
    color: #5836A3 !important;
    font-weight: 700 !important;
    font-size: 23px !important;
    margin-top: 22px !important;
}

/* Description text */
.stApp p {
    font-size: 17px;
    line-height: 1.7;
}

/* Form labels */
.stApp label {
    font-size: 16px !important;
    font-weight: 600 !important;
    color: #49366F !important;
}

/* Input fields */
.stApp input {
    font-size: 16px !important;
    border-radius: 10px !important;
}

/* Dropdown fields */
.stApp [data-baseweb="select"] {
    border-radius: 10px !important;
    font-size: 16px !important;
}

/* Multiselect selected items */
.stApp [data-baseweb="tag"] {
    background-color: #7544C8 !important;
}

/* Number input controls */
.stApp [data-testid="stNumberInput"] button {
    border-radius: 8px !important;
}

/* Save button */
.stApp button[kind="primary"] {
    background: linear-gradient(
        90deg,
        #7544C8,
        #3478E5,
        #D65AAB
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;

    font-size: 17px !important;
    font-weight: 700 !important;

    padding: 12px !important;

    box-shadow: 0 5px 15px rgba(80, 55, 160, 0.20);

    transition: all 0.25s ease;
}

/* Save button hover */
.stApp button[kind="primary"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 9px 20px rgba(80, 55, 160, 0.30);
}

/* Success and error messages */
.stApp [data-testid="stAlert"] {
    border-radius: 12px !important;
    font-size: 16px !important;
}
/* Divider */
.stApp hr {
    border-color: rgba(117, 68, 200, 0.20);
}
/* Learner Setup background */
.stApp {
    background: linear-gradient(
        135deg,
        #F5EEFF,
        #EEF5FF,
        #FFF0F7
    );
}
/* Match the homepage sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #5536A5,
        #3478E5,
        #D65AAB
    );
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* Consistent sidebar navigation */
[data-testid="stSidebarNav"] a {
    color: white !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    border-radius: 9px !important;
    transition: all 0.25s ease;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255, 255, 255, 0.20) !important;
    transform: translateX(3px);
}
/* Selected page */
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.28) !important;
    border-left: 4px solid #FFE5B4 !important;
}

/* Better form field appearance */
.stApp input,
.stApp textarea,
.stApp [data-baseweb="select"] {
    border-radius: 10px !important;
}
/* Subject Selection card */
.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        120deg,
        #E4D8FF,
        #DCE9FF,
        #FFE0EF
    ) !important;
    border: 1px solid #BFA6ED !important;
    border-radius: 18px !important;
    box-shadow: 0 7px 20px rgba(80, 55, 160, 0.18) !important;
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
.stApp [data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 26px rgba(80, 55, 160, 0.25) !important;
}

</style>
""", unsafe_allow_html=True)
# Page heading
st.title("👩‍🎓 Learner Setup")
st.write(
    "Let's understand your learning goals "
    "and create a personalized learning journey."
)
# Subject selection card
with st.container(border=True):
    st.subheader("📚 What subjects do you want to learn?")
    available_subjects = [
        "Python",
        "Biology",
        "Physics",
        "Chemistry",
        "Mathematics",
        "English",
        "Computer Science",
        "General Knowledge",
        "Other"
    ]
    selected_subjects = st.multiselect(
        "Select one or more subjects",
        available_subjects,
        placeholder="Choose your learning subjects..."
    )
    custom_subject = ""
    if "Other" in selected_subjects:
        custom_subject = st.text_input(
            "Enter your custom subject",
            placeholder="Example: Data Science"
        )
# Learning Goal card
with st.container(border=True):
    st.subheader("🎯 What is your learning goal?")
    learning_goal = st.text_input(
        "Enter your learning goal",
        placeholder="Example: Become a Python Developer..."
    )
# Current Learning Level card
with st.container(border=True):
    st.subheader("📊 What is your current learning level?")
    current_level = st.selectbox(
        "Select your learning level",
        ["Beginner", "Intermediate", "Advanced"],
        index=0
    )
# Target Duration card
with st.container(border=True):
    st.subheader("📅 How many days do you want to study?")
    target_days = st.number_input(
        "Select your target duration (days)",
        min_value=1,
        max_value=365,
        value=30,
        step=1
    )
# Daily Study Time card
with st.container(border=True):
    st.subheader("⏰ How much time can you study daily?")
    daily_hours = st.number_input(
        "Select your daily study hours",
        min_value=0.5,
        max_value=12.0,
        value=2.0,
        step=0.5
    )
# Save Learner Profile card
st.divider()
with st.container(border=True):
    st.subheader("💾 Save Your Learning Profile")
    if st.button(
        "💾 Save Learning Profile",
        type="primary",
        use_container_width=True
    ):
        subjects_to_save = [
            subject for subject in selected_subjects
            if subject != "Other"
        ]
        if "Other" in selected_subjects:
            if not custom_subject.strip():
                st.error("Please enter your custom subject.")
            else:
                subjects_to_save.append(custom_subject.strip())
        if not selected_subjects:
            st.error("Please select at least one subject.")

        elif "Other" in selected_subjects and not custom_subject.strip():
            pass

        elif not learning_goal.strip():
            st.error("Please enter your learning goal.")
        else:
            try:
                create_tables()
                saved_profiles = []
                for subject in subjects_to_save:
                    learner_id = save_learner(
                        subject,
                        learning_goal.strip(),
                        current_level,
                        target_days,
                        daily_hours
                    )
                    saved_profiles.append(
                        (subject, learner_id)
                    )
                st.success(
                    "🎉 Your learning profiles have been saved!"
                )
                st.subheader("📚 Saved Subjects")
                for subject, learner_id in saved_profiles:
                    st.write(
                        f"✅ {subject} — Learner ID: {learner_id}"
                    )
            except Exception as e:
                st.error(f"Unable to save your profiles: {e}")