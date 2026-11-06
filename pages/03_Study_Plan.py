
import streamlit as st
import sys
import re
from pathlib import Path

# Access project modules
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.db import (
    get_all_learners,
    save_study_plan,
    get_latest_study_plan,
    create_study_progress_table,
    get_study_progress,
    set_study_day_completion
)

from services.study_plan_service import create_personalized_plan


# Configure page
st.set_page_config(
    page_title="Personalized Study Plan",
    page_icon="📅",
    layout="wide"
)


# Save checkbox changes to SQLite
def update_day_progress(
    learner_id,
    plan_id,
    day_number,
    widget_key
):
    completed = st.session_state[widget_key]

    set_study_day_completion(
        learner_id,
        plan_id,
        day_number,
        completed
    )


# Extract day headings from the saved study plan
def extract_study_days(plan_text):

    pattern = re.compile(
        r"^\s*(?:[-*]\s*)?(?:#{1,6}\s*)?(?:\*\*)?"
        r"Day\s+(\d+)\s*:\s*(.*?)\s*(?:\*\*)?\s*$",
        re.IGNORECASE | re.MULTILINE
    )

    days = {}

    for match in pattern.finditer(plan_text):

        day_number = int(match.group(1))
        topic = match.group(2).strip().rstrip("*").strip()

        if day_number not in days:
            days[day_number] = topic

    return sorted(days.items())


# Page heading
st.title("📅 Your Personalized Study Plan")

st.write(
    "Generate a customized learning schedule "
    "based on your subject, goals and available study time."
)

st.divider()


# Retrieve all learner profiles
learners = get_all_learners()

st.subheader("📚 Select Your Learning Subject")

if not learners:

    st.warning(
        "No learner profile found. "
        "Please complete Learner Setup first."
    )

    st.stop()


# Keep the latest learner profile for each subject
learners_sorted = sorted(
    learners,
    key=lambda item: int(item["id"]),
    reverse=True
)

learners_by_subject = {}

for item in learners_sorted:

    subject_name = item["subject"].strip()

    subject_key = subject_name.lower()

    if subject_key not in learners_by_subject:
        learners_by_subject[subject_key] = item


# Subject dropdown
subject_options = list(learners_by_subject.keys())

selected_subject = st.selectbox(
    "Choose the subject you want to study:",
    options=subject_options,
    format_func=lambda subject: learners_by_subject[subject]["subject"],
    key="study_plan_subject_selector"
)

learner = learners_by_subject[selected_subject]


# Create progress table if it does not exist
create_study_progress_table()


# Display selected learner profile
st.divider()

st.subheader("👩‍🎓 Your Learning Profile")

st.success(
    "Your learner profile was retrieved successfully!"
)

col1, col2 = st.columns(2)

with col1:

    st.write("📚 **Subject:**", learner["subject"])

    st.write(
        "🎯 **Learning Goal:**",
        learner["learning_goal"]
    )

    st.write(
        "📊 **Current Level:**",
        learner["current_level"]
    )

with col2:

    st.write(
        "📅 **Target Duration:**",
        f'{learner["target_days"]} days'
    )

    st.write(
        "⏰ **Daily Study Time:**",
        f'{learner["daily_hours"]} hours'
    )


# Generate personalized study plan
st.divider()

st.subheader("🤖 Generate Your AI Study Plan")

if st.button(
    "✨ Generate Personalized Study Plan",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        f"🤖 Gemini is preparing your {learner['subject']} study plan..."
    ):

        try:

            study_plan = create_personalized_plan(learner)

            plan_id = save_study_plan(
                learner["id"],
                study_plan
            )

            st.success(
                f"🎉 Study plan saved successfully! Plan ID: {plan_id}"
            )

            st.rerun()

        except Exception as error:

            st.error(
                f"Study plan generation failed: {error}"
            )


# Display saved study plan for selected subject
saved_plan = get_latest_study_plan(learner["id"])

if saved_plan is not None:

    st.divider()

    st.subheader("📊 Your Study Progress")

    plan_id = saved_plan["id"]

    # Read saved progress from SQLite
    progress = get_study_progress(plan_id)

    # Extract study days from saved roadmap
    study_days = extract_study_days(
        saved_plan["plan_text"]
    )

    if study_days:

        total_days = len(study_days)

        completed_days = sum(
            1
            for day_number, topic in study_days
            if progress.get(day_number, False)
        )

        remaining_days = total_days - completed_days

        completion_percentage = (
            completed_days / total_days
        ) * 100 if total_days else 0

        # Progress summary cards
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "📅 Total Study Days",
            total_days
        )

        col2.metric(
            "✅ Completed Days",
            completed_days
        )

        col3.metric(
            "⏳ Remaining Days",
            remaining_days
        )

        st.write(
            f"**Overall Completion: {completion_percentage:.1f}%**"
        )

        st.progress(completion_percentage / 100)

        st.divider()

        st.subheader("☑️ Mark Your Daily Progress")

        st.write(
            "Tick the checkbox after completing that day's learning activities. "
            "Your progress will be saved automatically."
        )

        # Display a checkbox for every study day
        for day_number, topic in study_days:

            widget_key = (
                f"study_plan_{plan_id}_day_{day_number}"
            )

            # Load saved checkbox state
            if widget_key not in st.session_state:

                st.session_state[widget_key] = (
                    progress.get(day_number, False)
                )

            st.checkbox(
                f"Day {day_number}: {topic}",
                key=widget_key,
                on_change=update_day_progress,
                args=(
                    learner["id"],
                    plan_id,
                    day_number,
                    widget_key
                )
            )

        if completed_days == total_days:

            st.success(
                "🎉 Congratulations! You completed your entire study plan!"
            )

        elif completed_days > 0:

            st.info(
                f"Great progress! You have completed "
                f"{completed_days} out of {total_days} study days."
            )

        else:

            st.info(
                "Start your learning journey by completing Day 1!"
            )

    else:

        st.warning(
            "No day-wise headings were found in this study plan. "
            "Please check the study plan format."
        )

    # Display complete roadmap
    st.divider()

    st.subheader("📅 Your Saved Learning Roadmap")

    st.markdown(saved_plan["plan_text"])

else:

    st.info(
        f"No saved study plan found for {learner['subject']}. "
        "Generate your plan first."
    )
