
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


# Dashboard heading
st.title("📊 AI Learning Dashboard")

st.write(
    "Track your learning journey, study goals, "
    "and academic performance across all your subjects."
)

st.divider()


# Retrieve all learner profiles
learners = get_all_learners()

if not learners:

    st.warning("Please complete Learner Setup first.")

else:

    # Subject selection
    st.subheader("📚 Select Your Learning Subject")

    unique_learners = {}

    for learner_item in learners:
        unique_learners[
            learner_item["subject"].strip().lower()
        ] = learner_item

    learner_options = list(unique_learners.values())

    selected_subject = st.selectbox(
        "Choose a subject to view its dashboard",
        options=learner_options,
        format_func=lambda item: (
            f"{item['subject']} (Learner ID: {item['id']})"
        )
    )

    learner = selected_subject

    # Get selected learner data
    quiz_history = get_quiz_history(learner["id"])

    study_plan = get_latest_study_plan(learner["id"])

    progress_data = {}

    if study_plan:
        progress_data = get_study_progress(study_plan["id"])

    st.divider()

    # Learner Profile
    st.subheader("👤 Learner Profile")

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Subject:** {learner['subject']}")
        st.write(f"**Learning Goal:** {learner['learning_goal']}")
        st.write(f"**Current Level:** {learner['current_level']}")

    with col2:
        st.write(f"**Target Duration:** {learner['target_days']} days")
        st.write(f"**Daily Study Time:** {learner['daily_hours']} hours")
        st.write(f"**Learner ID:** {learner['id']}")

    st.divider()

    # Study Plan Progress
    st.subheader("📅 Study Plan Progress")

    if study_plan:

        total_days = learner["target_days"]

        completed_days = sum(
            1 for completed in progress_data.values() if completed
        )

        remaining_days = max(total_days - completed_days, 0)

        completion_percentage = (
            completed_days / total_days
        ) * 100 if total_days else 0

        col1, col2, col3 = st.columns(3)

        col1.metric("📚 Total Study Days", total_days)
        col2.metric("✅ Completed Days", completed_days)
        col3.metric("⏳ Remaining Days", remaining_days)

        st.markdown(
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

    st.divider()

    # Quiz Performance
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

        col1, col2, col3 = st.columns(3)

        col1.metric("📝 Total Quiz Attempts", total_attempts)
        col2.metric("📈 Average Accuracy", f"{average_accuracy:.1f}%")
        col3.metric("🥇 Best Accuracy", f"{best_accuracy:.1f}%")

    else:

        st.info(
            f"Complete a {learner['subject']} quiz to see "
            "your performance here."
        )

    # Strong and Weak Topic Analysis
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

            st.markdown("### 🔴 Weak Topics")

            if weak_topics:
                for topic in weak_topics:
                    st.error(
                        f"{topic['topic']} — "
                        f"{topic['accuracy']:.1f}%"
                    )
            else:
                st.info("No weak topics identified yet.")

        # Personalized recommendations
        st.divider()

        st.subheader("💡 Personalized Learning Recommendations")

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

    # Quiz Accuracy Progress Chart
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

        st.line_chart(
            chart_df.set_index("Quiz Attempt")["Accuracy"],
            y_label="Accuracy (%)"
        )

    # Downloadable PDF Learning Progress Report
    st.divider()

    st.subheader("📄 Download Learning Progress Report")

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
