
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

# Page heading
st.title("👩‍🎓 Learner Setup")

st.write(
    "Let's understand your learning goals "
    "and create a personalized learning journey."
)

# Subject selection
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

# Learning Goal
st.subheader("🎯 What is your learning goal?")

learning_goal = st.text_input(
    "Enter your learning goal",
    placeholder="Example: Become a Python Developer..."
)

# Current Learning Level
st.subheader("📊 What is your current learning level?")

current_level = st.selectbox(
    "Select your learning level",
    ["Beginner", "Intermediate", "Advanced"],
    index=0
)

# Target Duration
st.subheader("📅 How many days do you want to study?")

target_days = st.number_input(
    "Select your target duration (days)",
    min_value=1,
    max_value=365,
    value=30,
    step=1
)

# Daily Study Time
st.subheader("⏰ How much time can you study daily?")

daily_hours = st.number_input(
    "Select your daily study hours",
    min_value=0.5,
    max_value=12.0,
    value=2.0,
    step=0.5
)

# Save Learner Profile
st.divider()

st.subheader("💾 Save Your Learning Profile")

if st.button(
    "Save Learning Profile",
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
