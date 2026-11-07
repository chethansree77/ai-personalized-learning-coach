
import streamlit as st
import sys
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Learning Dashboard",
    page_icon="📊",
    layout="wide"
)

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.db import (
    get_all_learners,
    get_quiz_history,
    get_latest_study_plan,
    get_study_progress
)

from services.report_generator import generate_progress_report


# --------------------------------------------------
# DASHBOARD STYLING
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

/* Main heading */
h1 {
    color: #5636A8 !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
}

/* Section headings */
h2, h3 {
    color: #5636A8 !important;
    font-weight: 750 !important;
}

/* Text readability */
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #26365C;
    font-size: 1rem;
    line-height: 1.65;
}

/* All bordered cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #D8C5FF !important;
    border-radius: 15px !important;
    background: linear-gradient(
        135deg,
        rgba(247, 243, 255, 0.96),
        rgba(232, 241, 255, 0.96)
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
    font-size: 2rem !important;
    font-weight: 800 !important;
}

/* Select box */
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #F1F3FA;
    border-radius: 10px;
    min-height: 45px;
    font-size: 1rem;
}

/* Single Study Progress Bar */
[data-testid="stProgressBar"] {
    width: 100% !important;
}

[data-testid="stProgressBar"] > div {
    background: #E8EAF5 !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    height: 12px !important;
}

[data-testid="stProgressBar"] [role="progressbar"] {
    border-radius: 20px !important;
}

/* Success, warning and information messages */
[data-testid="stAlert"] {
    border-radius: 12px;
    font-size: 1rem;
}

/* Recommendations */
[data-testid="stAlert"] p {
    font-size: 0.98rem !important;
    line-height: 1.6;
}

/* Chart container */
[data-testid="stVegaLiteChart"],
[data-testid="stArrowVegaLiteChart"] {
    background: rgba(255, 255, 255, 0.55);
    border: 1px solid #D8C5FF;
    border-radius: 14px;
    padding: 14px;
    box-shadow: 0 4px 12px rgba(83, 55, 160, 0.07);
}

/* Download button */
.stDownloadButton button {
    background: linear-gradient(
        110deg,
        #7542D0,
        #3978E8,
        #DB55AC
    ) !important;
    color: white !important;
    border: none !important;
    border-radius: 11px !important;
    min-height: 48px;
    font-size: 1rem !important;
    font-weight: 700 !important;
    transition: all 0.25s ease;
}

.stDownloadButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 18px rgba(83, 55, 160, 0.22);
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

/* Responsive layout */
@media (max-width: 768px) {
    h1 {
        font-size: 2rem !important;
    }

    h2, h3 {
        font-size: 1.3rem !important;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
    }
}

/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
    [data-testid="stVerticalBlockBorderWrapper"],
    .stDownloadButton button {
        transition: none !important;
    }
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DASHBOARD HEADING
# --------------------------------------------------

st.title("📊 AI Learning Dashboard")

st.write(
    "Track your learning journey, study goals, "
    "and academic performance across all your subjects."
)

st.divider()


# --------------------------------------------------
# RETRIEVE LEARNER PROFILES
# --------------------------------------------------

learners = get_all_learners()

if not learners:

    st.warning("Please complete Learner Setup first.")

else:

    # Keep the latest learner profile for each subject
    learners_sorted = sorted(
        learners,
        key=lambda item: int(item["id"]),
        reverse=True
    )

    unique_learners = {}

    for learner_item in learners_sorted:

        subject_key = learner_item["subject"].strip().lower()

        if subject_key not in unique_learners:
            unique_learners[subject_key] = learner_item

    learner_options = list(unique_learners.values())


    # --------------------------------------------------
    # SUBJECT SELECTION
    # --------------------------------------------------

    with st.container(border=True):

        st.subheader("📚 Select Your Learning Subject")

        selected_subject = st.selectbox(
            "Choose a subject to view its dashboard",
            options=learner_options,
            format_func=lambda item: (
                f"{item['subject']} (Learner ID: {item['id']})"
            ),
            key="dashboard_subject_selector"
        )

        learner = selected_subject

        st.success(
            f"Selected Subject: {learner['subject']}"
        )


    # --------------------------------------------------
    # RETRIEVE SELECTED LEARNER DATA
    # --------------------------------------------------

    quiz_history = get_quiz_history(learner["id"])

    study_plan = get_latest_study_plan(learner["id"])

    progress_data = {}

    if study_plan:
        progress_data = get_study_progress(study_plan["id"])


    # --------------------------------------------------
    # LEARNER PROFILE
    # --------------------------------------------------

    st.divider()

    st.subheader("👤 Learner Profile")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:

            st.write(f"**📚 Subject:** {learner['subject']}")

            st.write(
                f"**🎯 Learning Goal:** {learner['learning_goal']}"
            )

            st.write(
                f"**📊 Current Level:** {learner['current_level']}"
            )

        with col2:

            st.write(
                f"**📅 Target Duration:** {learner['target_days']} days"
            )

            st.write(
                f"**⏰ Daily Study Time:** {learner['daily_hours']} hours"
            )

            st.write(
                f"**🆔 Learner ID:** {learner['id']}"
            )


    # --------------------------------------------------
    # STUDY PLAN PROGRESS
    # --------------------------------------------------

    st.divider()

    st.subheader("📅 Study Plan Progress")

    if study_plan:

        total_days = learner["target_days"]

        completed_days = sum(
            1 for completed in progress_data.values()
            if completed
        )

        remaining_days = max(
            total_days - completed_days,
            0
        )

        completion_percentage = (
            completed_days / total_days
        ) * 100 if total_days else 0


        with st.container(border=True):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📚 Total Study Days",
                    total_days
                )

            with col2:
                st.metric(
                    "✅ Completed Days",
                    completed_days
                )

            with col3:
                st.metric(
                    "⏳ Remaining Days",
                    remaining_days
                )

            st.write(
                f"**Overall Completion: {completion_percentage:.1f}%**"
            )

            st.progress(completion_percentage / 100)

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

        st.info(
            f"No study plan found for {learner['subject']}. "
            "Generate a personalized study plan to track progress."
        )


    # --------------------------------------------------
    # QUIZ PERFORMANCE
    # --------------------------------------------------

    st.divider()

    st.subheader("🏆 Quiz Performance")

    if quiz_history:

        total_attempts = len(quiz_history)

        total_score = sum(
            row["score"] for row in quiz_history
        )

        total_questions = sum(
            row["total_questions"] for row in quiz_history
        )

        average_accuracy = (
            total_score / total_questions
        ) * 100 if total_questions else 0

        valid_accuracies = [
            (row["score"] / row["total_questions"]) * 100
            for row in quiz_history
            if row["total_questions"] > 0
        ]

        best_accuracy = max(valid_accuracies, default=0)


        with st.container(border=True):

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📝 Total Quiz Attempts",
                    total_attempts
                )

            with col2:
                st.metric(
                    "📈 Average Accuracy",
                    f"{average_accuracy:.1f}%"
                )

            with col3:
                st.metric(
                    "🥇 Best Accuracy",
                    f"{best_accuracy:.1f}%"
                )

    else:

        st.info(
            f"Complete a {learner['subject']} quiz to see "
            "your performance here."
        )


    # --------------------------------------------------
    # STRONG AND WEAK TOPIC ANALYSIS
    # --------------------------------------------------

    st.divider()

    st.subheader("🎯 Strong and Weak Topic Analysis")

    strong_topics = []
    improving_topics = []
    weak_topics = []

    if quiz_history:

        topic_stats = {}

        for row in quiz_history:

            topic_name = row["topic"].strip()
            topic_key = topic_name.lower()

            if topic_key not in topic_stats:

                topic_stats[topic_key] = {
                    "topic": topic_name,
                    "score": 0,
                    "total": 0
                }

            topic_stats[topic_key]["score"] += row["score"]

            topic_stats[topic_key]["total"] += row["total_questions"]


        for topic in topic_stats.values():

            accuracy = (
                topic["score"] / topic["total"]
            ) * 100 if topic["total"] else 0

            topic_result = {
                "topic": topic["topic"],
                "accuracy": accuracy
            }

            if accuracy >= 80:
                strong_topics.append(topic_result)

            elif accuracy >= 50:
                improving_topics.append(topic_result)

            else:
                weak_topics.append(topic_result)


        col1, col2, col3 = st.columns(3)

        with col1:

            with st.container(border=True):

                st.markdown("### 🟢 Strong Topics")

                if strong_topics:

                    for topic in strong_topics:

                        st.success(
                            f"{topic['topic']} — "
                            f"{topic['accuracy']:.1f}%"
                        )

                else:

                    st.info("No strong topics identified yet.")


        with col2:

            with st.container(border=True):

                st.markdown("### 🟡 Needs Improvement")

                if improving_topics:

                    for topic in improving_topics:

                        st.warning(
                            f"{topic['topic']} — "
                            f"{topic['accuracy']:.1f}%"
                        )

                else:

                    st.info("No topics in this category yet.")


        with col3:

            with st.container(border=True):

                st.markdown("### 🔴 Weak Topics")

                if weak_topics:

                    for topic in weak_topics:

                        st.error(
                            f"{topic['topic']} — "
                            f"{topic['accuracy']:.1f}%"
                        )

                else:

                    st.info("No weak topics identified yet.")


        # --------------------------------------------------
        # PERSONALIZED RECOMMENDATIONS
        # --------------------------------------------------

        st.divider()

        st.subheader("💡 Personalized Learning Recommendations")

        with st.container(border=True):

            for topic in weak_topics:

                st.error(
                    f"**{topic['topic']}:** Your accuracy is "
                    f"{topic['accuracy']:.1f}%. "
                    "Review the basics, study worked examples, "
                    "and practise more questions."
                )

            for topic in improving_topics:

                st.warning(
                    f"**{topic['topic']}:** You are making progress. "
                    "Revise important concepts and take another quiz "
                    "to improve your accuracy."
                )

            for topic in strong_topics:

                st.success(
                    f"**{topic['topic']}:** Great work! "
                    "Continue practising to maintain your performance."
                )

            st.caption(
                "Topic classifications are based on saved quiz results "
                "for the selected subject profile."
            )

    else:

        st.info(
            "Complete and submit a quiz to identify your strong "
            "and weak topics."
        )


    # --------------------------------------------------
    # QUIZ ACCURACY PROGRESS CHART
    # --------------------------------------------------

    if quiz_history:

        st.divider()

        st.subheader("📈 Your Quiz Accuracy Progress")

        chart_data = []

        for index, row in enumerate(
            reversed(quiz_history),
            start=1
        ):

            accuracy = (
                row["score"] / row["total_questions"]
            ) * 100 if row["total_questions"] else 0

            chart_data.append({
                "Quiz Attempt": f"Quiz {index}",
                "Accuracy": accuracy
            })

        chart_df = pd.DataFrame(chart_data)

        with st.container(border=True):

            st.line_chart(
                chart_df.set_index("Quiz Attempt")["Accuracy"],
                y_label="Accuracy (%)"
            )


    # --------------------------------------------------
    # DOWNLOADABLE PDF LEARNING PROGRESS REPORT
    # --------------------------------------------------

    st.divider()

    st.subheader("📄 Download Learning Progress Report")

    with st.container(border=True):

        st.write(
            "Generate a PDF report containing your learner profile, "
            "study progress, quiz performance and quiz history."
        )

        # Fill missing study days as incomplete.
        # This ensures the PDF uses the learner's full target duration.

        report_progress = {
            day: progress_data.get(day, False)
            for day in range(1, learner["target_days"] + 1)
        }

        try:

            pdf_data = generate_progress_report(
                learner=learner,
                study_plan=study_plan,
                study_progress=report_progress,
                quiz_history=quiz_history
            )

            filename = (
                f"{learner['subject'].replace(' ', '_')}"
                f"_Learning_Progress_Report.pdf"
            )

            st.download_button(
                label="📥 Download My Progress Report",
                data=pdf_data,
                file_name=filename,
                mime="application/pdf",
                use_container_width=True
            )

            st.caption(
                "Your report is generated using the saved information "
                "for the selected subject."
            )

        except Exception as error:

            st.error(
                f"Unable to generate the PDF report: {error}"
            )
