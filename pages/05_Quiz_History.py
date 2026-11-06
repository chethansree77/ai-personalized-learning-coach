import streamlit as st
import sys
import json
from pathlib import Path

st.set_page_config(
    page_title="Quiz History",
    page_icon="📊",
    layout="wide"
)

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.db import (
    get_all_learners,
    get_quiz_history
)


# Page heading
st.title("📊 Quiz History")

st.write(
    "View your previous quiz attempts and track your learning progress."
)

st.divider()

# Retrieve all learner profiles
learners = get_all_learners()

if not learners:

    st.warning("Please complete Learner Setup first.")

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
st.subheader("📚 Select Your Learning Subject")

subject_options = list(learners_by_subject.keys())

selected_subject = st.selectbox(
    "Choose the subject whose quiz history you want to view:",
    options=subject_options,
    format_func=lambda subject: learners_by_subject[subject]["subject"],
    key="quiz_history_subject_selector"
)

learner = learners_by_subject[selected_subject]

st.success(f"Learning Subject: {learner['subject']}")

# Retrieve saved quiz attempts for selected learner
history = get_quiz_history(learner["id"])

if not history:

    st.info(
        f"📚 No quiz history found for {learner['subject']}. "
        "Complete a quiz to see your progress here."
    )

else:

    # Calculate performance
    total_attempts = len(history)

    total_score = sum(row[2] for row in history)

    total_questions = sum(row[3] for row in history)

    average_accuracy = (
        total_score / total_questions
    ) * 100 if total_questions else 0

    valid_accuracies = [
        (row[2] / row[3]) * 100
        for row in history
        if row[3] > 0
    ]

    best_score = max(valid_accuracies, default=0)

    # Summary metrics
    st.subheader("🏆 Your Learning Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Quiz Attempts",
        total_attempts
    )

    col2.metric(
        "Average Accuracy",
        f"{average_accuracy:.1f}%"
    )

    col3.metric(
        "Best Accuracy",
        f"{best_score:.1f}%"
    )

    st.divider()

    # Quiz history
    st.subheader("📚 Previous Quiz Attempts")

    for row in history:

        attempt_id = row[0]
        topic = row[1]
        score = row[2]
        total = row[3]
        answers = row[4]
        created_at = row[5]
        quiz_mode = row[6]

        accuracy = (
            score / total
        ) * 100 if total else 0

        with st.expander(
            f"📘 {topic} | Score: {score}/{total} | {accuracy:.0f}%"
        ):

            st.write(f"**Attempt ID:** {attempt_id}")

            st.write(f"**Topic:** {topic}")

            st.write(f"**Date:** {created_at}")

            if quiz_mode == "Demo":

                st.warning("🧪 Demo Mode — Predefined Questions")

            else:

                st.success("🤖 AI Mode — Gemini Generated Questions")

            st.write(f"**Score:** {score}/{total}")

            st.write(f"**Accuracy:** {accuracy:.1f}%")

            try:

                answer_data = (
                    json.loads(answers)
                    if isinstance(answers, str)
                    else answers
                )

                st.write("**Submitted Answers:**")

                st.json(answer_data)

            except (ValueError, TypeError):

                st.write("Answer details are unavailable.")
