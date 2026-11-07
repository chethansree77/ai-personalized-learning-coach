
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


# --------------------------------------------------
# PAGE STYLING
# --------------------------------------------------

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        120deg,
        #EEF2FF 0%,
        #F5F0FF 55%,
        #FFF0F7 100%
    );
}

/* Main content spacing */
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

/* Page title */
h1 {
    color: #5535A5 !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

/* Section headings */
h2, h3 {
    color: #5636A8 !important;
    font-weight: 750 !important;
}

/* General text */
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #26365C;
    font-size: 1rem;
    line-height: 1.65;
}

/* Input fields */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #F1F3FA;
    border-radius: 10px;
    min-height: 45px;
    font-size: 1rem;
}

/* Summary card containers */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #D8C5FF !important;
    border-radius: 15px !important;
    background: linear-gradient(
        135deg,
        rgba(239, 233, 255, 0.95),
        rgba(231, 240, 255, 0.95)
    ) !important;
    box-shadow: 0 4px 12px rgba(83, 55, 160, 0.08);
    transition: transform 0.25s ease,
                box-shadow 0.25s ease,
                border-color 0.25s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 24px rgba(83, 55, 160, 0.16);
    border-color: #9870F5 !important;
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #5939A5 !important;
    font-size: 1rem !important;
    font-weight: 650 !important;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #315FCA !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
}

/* Quiz attempt expanders */
[data-testid="stExpander"] {
    border: 1px solid #D6C4FF !important;
    border-radius: 13px !important;
    background: rgba(255, 255, 255, 0.55);
    box-shadow: 0 3px 9px rgba(83, 55, 160, 0.06);
    transition: transform 0.25s ease,
                box-shadow 0.25s ease,
                border-color 0.25s ease;
    margin-bottom: 12px;
}

[data-testid="stExpander"]:hover {
    transform: translateY(-3px);
    border-color: #9365EE !important;
    box-shadow: 0 9px 20px rgba(83, 55, 160, 0.14);
}

/* Expander heading */
[data-testid="stExpander"] summary {
    color: #5636A8 !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 12px;
}

/* Expander content */
[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
    padding: 18px;
}

/* JSON display */
[data-testid="stJson"] {
    border-radius: 10px;
    border: 1px solid #D8C5FF;
    background: rgba(255, 255, 255, 0.65);
}

/* Success and warning messages */
[data-testid="stAlert"] {
    border-radius: 12px;
    font-size: 1rem;
}

/* Dividers */
hr {
    border-color: #D5C7F2 !important;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #5036A6 0%,
        #3475E2 55%,
        #B75AB8 100%
    );
}

[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton button {
    border-radius: 10px;
    transition: all 0.25s ease;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 14px rgba(83, 55, 160, 0.18);
}

/* Responsive headings */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }

    h2, h3 {
        font-size: 1.3rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
    }
}

@media (prefers-reduced-motion: reduce) {
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stExpander"],
    .stButton button {
        transition: none !important;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def get_value(row, key, index):
    if isinstance(row, dict):
        return row[key]
    return row[index]


# --------------------------------------------------
# PAGE HEADING
# --------------------------------------------------

st.title("📊 Quiz History")

st.write(
    "View your previous quiz attempts and track your learning progress."
)

st.divider()


# --------------------------------------------------
# RETRIEVE LEARNER PROFILES
# --------------------------------------------------

learners = get_all_learners()

if not learners:
    st.warning("Please complete Learner Setup first.")
    st.stop()


# Keep latest learner profile for each subject

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


# --------------------------------------------------
# SUBJECT SELECTION CARD
# --------------------------------------------------

with st.container(border=True):

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


# --------------------------------------------------
# RETRIEVE QUIZ HISTORY
# --------------------------------------------------

history = get_quiz_history(learner["id"])


if not history:

    st.info(
        f"📚 No quiz history found for {learner['subject']}. "
        "Complete a quiz to see your progress here."
    )

else:

    # --------------------------------------------------
    # PERFORMANCE CALCULATIONS
    # --------------------------------------------------

    total_attempts = len(history)

    total_score = sum(
        get_value(row, "score", 2)
        for row in history
    )

    total_questions = sum(
        get_value(row, "total_questions", 3)
        for row in history
    )

    average_accuracy = (
        total_score / total_questions
    ) * 100 if total_questions else 0

    valid_accuracies = [
        (
            get_value(row, "score", 2)
            / get_value(row, "total_questions", 3)
        ) * 100
        for row in history
        if get_value(row, "total_questions", 3) > 0
    ]

    best_score = max(valid_accuracies, default=0)


    # --------------------------------------------------
    # LEARNING SUMMARY
    # --------------------------------------------------

    st.divider()

    st.subheader("🏆 Your Learning Summary")

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.metric(
                "📚 Total Quiz Attempts",
                total_attempts
            )

    with col2:

        with st.container(border=True):

            st.metric(
                "📈 Average Accuracy",
                f"{average_accuracy:.1f}%"
            )

    with col3:

        with st.container(border=True):

            st.metric(
                "🏆 Best Accuracy",
                f"{best_score:.1f}%"
            )


    # --------------------------------------------------
    # PREVIOUS QUIZ ATTEMPTS
    # --------------------------------------------------

    st.divider()

    st.subheader("📚 Previous Quiz Attempts")

    for row in history:

        attempt_id = get_value(row, "id", 0)
        topic = get_value(row, "topic", 1)
        score = get_value(row, "score", 2)
        total = get_value(row, "total_questions", 3)
        answers = get_value(row, "answers", 4)
        created_at = get_value(row, "created_at", 5)
        quiz_mode = get_value(row, "quiz_mode", 6)

        accuracy = (
            score / total
        ) * 100 if total else 0


        with st.expander(
            f"📘 {topic} | Score: {score}/{total} | {accuracy:.0f}%"
        ):

            detail_col1, detail_col2 = st.columns(2)

            with detail_col1:

                st.write(f"**Attempt ID:** {attempt_id}")
                st.write(f"**Topic:** {topic}")

            with detail_col2:

                st.write(f"**Date:** {created_at}")
                st.write(f"**Score:** {score}/{total}")
                st.write(f"**Accuracy:** {accuracy:.1f}%")


            if quiz_mode == "Demo":

                st.warning(
                    "🧪 Demo Mode — Predefined Questions"
                )

            else:

                st.success(
                    "🤖 AI Mode — Gemini Generated Questions"
                )


            st.divider()

            st.write("### 📝 Submitted Answers")

            try:

                answer_data = (
                    json.loads(answers)
                    if isinstance(answers, str)
                    else answers
                )

                st.json(answer_data)

            except (ValueError, TypeError):

                st.write("Answer details are unavailable.")
