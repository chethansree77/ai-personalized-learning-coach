
import streamlit as st
import sys
from pathlib import Path

st.set_page_config(
    page_title="Practice Quiz",
    page_icon="📝",
    layout="wide"
)

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.db import (
    get_all_learners,
    create_quiz_table,
    save_quiz_attempt
)

from services.quiz_service import generate_quiz
from services.demo_quiz_service import generate_demo_quiz


def display_theory_explanation(explanation):

    st.markdown("### 💡 Understand the Concept")
    st.write(explanation["concept"])

    st.markdown("### ⭐ Important Points")

    for point in explanation["key_points"]:
        st.markdown(f"- {point}")

    st.markdown("### 💻 Practical Example")
    st.info(explanation["example"])

    st.markdown("### 🔍 Understand the Options")

    option_analysis = explanation["option_analysis"]

    for option in ["A", "B", "C", "D"]:

        if option in option_analysis:
            st.markdown(f"**Option {option}**")
            st.write(option_analysis[option])

    st.markdown("### 🧠 Memory Tip")
    st.success(explanation["memory_tip"])


def display_maths_explanation(explanation):

    import re

    def clean_text(value):
        return re.sub(r"\s+", " ", str(value)).strip()

    # Formula card
    st.markdown("### 📌 Important Formula")

    with st.container(border=True):

        st.markdown("#### 🧮 Remember this formula")

        st.markdown(
            f"### {clean_text(explanation['formula'])}"
        )

    # Symbols
    st.markdown("### 🔤 Understand the Symbols")

    with st.container(border=True):

        for symbol in explanation["symbols"]:
            st.markdown(f"- {clean_text(symbol)}")

    # Given values
    st.markdown("### 📝 Given Values")

    with st.container(border=True):

        for value in explanation["given_values"]:
            st.markdown(f"- {clean_text(value)}")

    # Step-by-step solution
    st.markdown("### 🪜 Step-by-Step Solution")

    for index, step in enumerate(explanation["steps"], start=1):

        with st.container(border=True):

            st.markdown(f"**STEP {index}**")
            st.write(clean_text(step))

    # Reasoning
    st.markdown("### 💡 Why This Method Works")
    st.info(clean_text(explanation["reasoning"]))

    # Shortcut
    st.markdown("### ⚡ Shortcut Method")

    with st.container(border=True):
        st.write(clean_text(explanation["shortcut"]))

    # Final answer
    st.markdown("### 🎯 Final Answer")
    st.success(clean_text(explanation["final_answer"]))

    # Memory tip
    st.markdown("### 🧠 Memory Tip")
    st.info(clean_text(explanation["memory_tip"]))


# Page heading
st.title("📝 AI Practice Quiz")

st.write(
    "Choose a topic and practice with five "
    "AI-generated multiple-choice questions."
)


# Retrieve all learner profiles
learners = get_all_learners()

# Create quiz history table
create_quiz_table()


if not learners:

    st.warning("Please complete Learner Setup first.")

else:

    # Keep the newest learner profile for each subject.
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

    st.subheader("📚 Select Your Learning Subject")

    subject_options = list(learners_by_subject.keys())

    selected_subject = st.selectbox(
        "Choose the subject for your practice quiz:",
        options=subject_options,
        format_func=lambda subject: learners_by_subject[subject]["subject"],
        key="practice_quiz_subject_selector"
    )

    learner = learners_by_subject[selected_subject]

    # Clear an old quiz when the learner changes, so results from one
    # subject are never displayed or saved under another subject.
    previous_quiz_learner = st.session_state.get("quiz_learner_id")

    if previous_quiz_learner != learner["id"]:
        quiz_state_keys = [
            "quiz_questions",
            "quiz_topic",
            "quiz_type",
            "quiz_mode",
            "quiz_submitted",
            "quiz_score",
            "quiz_answers",
            "quiz_saved",
            "quiz_learner_id"
        ]

        for state_key in quiz_state_keys:
            st.session_state.pop(state_key, None)

        for question_number in range(1, 6):
            st.session_state.pop(f"question_{question_number}", None)

    st.success(f"Learning Subject: {learner['subject']}")

    # Topic selection
    topic = st.text_input(
        "📚 Enter the topic you want to practice",
        placeholder="Example: Python Variables, Loops, Functions..."
    )

    # Question type
    question_type = st.selectbox(
        "📖 Select question type",
        ["Theory", "Maths / Aptitude"]
    )

    # Generate quiz
    if st.button(
        "✨ Generate 5 Questions",
        type="primary",
        use_container_width=True
    ):

        if not topic.strip():

            st.error("Please enter a topic.")

        else:

            with st.spinner(
                "🤖 Preparing your practice questions..."
            ):

                try:

                    # First, try Gemini AI.
                    questions = generate_quiz(
                        subject=learner["subject"],
                        topic=topic.strip(),
                        level=learner["current_level"],
                        question_type=question_type
                    )

                    quiz_mode = "AI"

                except Exception as gemini_error:

                    # If Gemini fails, load predefined demo questions.
                    try:

                        questions = generate_demo_quiz(
                            subject=learner["subject"],
                            topic=topic.strip(),
                            level=learner["current_level"],
                            question_type=question_type
                        )

                        quiz_mode = "Demo"

                    except Exception as demo_error:

                        st.error(
                            "Both AI quiz generation and demo "
                            "quiz loading failed."
                        )

                        st.error(f"Gemini error: {gemini_error}")
                        st.error(f"Demo error: {demo_error}")

                        questions = None
                        quiz_mode = None

                if questions is not None:

                    st.session_state["quiz_questions"] = questions
                    st.session_state["quiz_topic"] = topic.strip()
                    st.session_state["quiz_type"] = question_type
                    st.session_state["quiz_mode"] = quiz_mode
                    st.session_state["quiz_learner_id"] = learner["id"]

                    # Reset previous quiz results
                    st.session_state["quiz_submitted"] = False

                    st.session_state.pop("quiz_score", None)
                    st.session_state.pop("quiz_answers", None)
                    st.session_state["quiz_saved"] = False

                    # Clear previous radio selections
                    for i in range(1, 6):
                        st.session_state.pop(f"question_{i}", None)

                    if quiz_mode == "AI":

                        st.success(
                            "🎉 Your five AI-generated questions are ready!"
                        )

                    else:

                        st.warning(
                            "⚠️ Gemini is currently unavailable. "
                            "Demo Mode is active. These are predefined "
                            "practice questions, not AI-generated "
                            "questions for your selected topic."
                        )


    # Display quiz outside Generate button
    if "quiz_questions" in st.session_state:

        st.divider()

        st.subheader("🎯 Your Practice Questions")

        if st.session_state.get("quiz_mode") == "Demo":

            st.info("🧪 Demo Mode — Predefined practice questions")

        else:

            st.success("🤖 AI Mode — Gemini-generated questions")

        answers = {}

        quiz_already_submitted = st.session_state.get(
            "quiz_submitted", False
        )

        # Quiz form
        with st.form("quiz_form"):

            for index, question in enumerate(
                st.session_state["quiz_questions"],
                start=1
            ):

                st.write(
                    f"**Question {index}: {question['question']}**"
                )

                selected_answer = st.radio(
                    f"Choose your answer for Question {index}",
                    options=["A", "B", "C", "D"],
                    index=None,
                    format_func=lambda option, q=question: (
                        f"{option}. {q['options'][option]}"
                    ),
                    key=f"question_{index}",
                    disabled=quiz_already_submitted
                )

                answers[index] = selected_answer

            st.divider()

            submitted = st.form_submit_button(
                "📝 Submit Quiz",
                type="primary",
                use_container_width=True,
                disabled=quiz_already_submitted
            )

        # Validate submitted answers
        if submitted:

            if any(answer is None for answer in answers.values()):

                st.warning(
                    "⚠️ Please answer all five questions before submitting."
                )

            else:

                score = 0

                for index, question in enumerate(
                    st.session_state["quiz_questions"],
                    start=1
                ):

                    if answers[index] == question["correct_answer"]:
                        score += 1

                st.session_state["quiz_answers"] = answers.copy()
                st.session_state["quiz_score"] = score
                st.session_state["quiz_submitted"] = True

                # Save quiz attempt in SQLite
                try:

                    save_quiz_attempt(
                        learner["id"],
                        st.session_state["quiz_topic"],
                        score,
                        len(st.session_state["quiz_questions"]),
                        answers,
                        quiz_mode=st.session_state.get("quiz_mode", "AI")
                    )

                    st.session_state["quiz_saved"] = True

                except Exception as error:

                    st.session_state["quiz_saved"] = False

                    st.error(
                        f"Quiz result could not be saved: {error}"
                    )

                st.rerun()

        # Display results after submission
        if st.session_state.get("quiz_submitted", False):

            score = st.session_state["quiz_score"]

            total_questions = len(
                st.session_state["quiz_questions"]
            )

            percentage = (
                score / total_questions
            ) * 100

            st.divider()

            st.subheader("🏆 Your Quiz Results")

            st.success(
                f"🎉 Your Score: {score}/{total_questions}"
            )

            st.progress(percentage / 100)

            st.write(
                f"**Your Accuracy: {percentage:.0f}%**"
            )

            if st.session_state.get("quiz_mode") == "Demo":

                st.caption(
                    "This result came from a predefined demo quiz."
                )

            if st.session_state.get("quiz_saved", False):

                st.success(
                    "💾 Your quiz attempt has been saved successfully!"
                )

            st.divider()

            st.subheader("📖 Detailed Answer Review")

            for index, question in enumerate(
                st.session_state["quiz_questions"],
                start=1
            ):

                correct_answer = question["correct_answer"]
                correct_text = question["options"][correct_answer]

                selected_answer = st.session_state[
                    "quiz_answers"
                ][index]

                with st.expander(
                    f"Question {index}: {question['question']}",
                    expanded=True
                ):

                    st.write(
                        f"**Your answer:** {selected_answer}. "
                        f"{question['options'][selected_answer]}"
                    )

                    st.write(
                        f"**Correct answer:** {correct_answer}. "
                        f"{correct_text}"
                    )

                    if selected_answer == correct_answer:

                        st.success("✅ Correct answer!")

                    else:

                        st.error("❌ Incorrect answer!")

                    st.divider()

                    if st.session_state["quiz_type"] == "Theory":

                        display_theory_explanation(
                            question["explanation"]
                        )

                    else:

                        display_maths_explanation(
                            question["explanation"]
                        )
