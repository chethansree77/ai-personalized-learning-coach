
import streamlit as st
import sys
from pathlib import Path
st.set_page_config(
    page_title="Practice Quiz",
    page_icon="📝",
    layout="wide"
)
st.markdown("""
<style>
/* Practice Quiz - Purple Blue Pink Theme */
.stApp {
    background: linear-gradient(
        135deg,
        #F5EEFF,
        #EEF5FF,
        #FFF0F7
    );
}
/* Headings */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4 {
    color: #5836A3 !important;
    font-weight: 800 !important;
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #5536A5,
        #3478E5,
        #B65DB8
    ) !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a *,
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] p {
    color: white !important;
    -webkit-text-fill-color: white !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.20) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255,255,255,0.30) !important;
    border-left: 4px solid #FFE082 !important;
    border-radius: 8px !important;
}
/* Cards */
.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #D5C5F2 !important;
    border-radius: 16px !important;
    background: rgba(255,255,255,0.48) !important;
    box-shadow: 0 5px 15px rgba(80,55,160,0.09);
    transition: transform 0.25s ease,
                box-shadow 0.25s ease,
                border-color 0.25s ease;
}
.stApp [data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    border-color: #9875DA !important;
    box-shadow: 0 10px 22px rgba(80,55,160,0.17);
}
/* Input fields */
.stApp input,
.stApp textarea,
.stApp [data-baseweb="select"] > div {
    border-radius: 10px !important;
}
.stApp input:focus,
.stApp textarea:focus {
    border-color: #7544C8 !important;
}
/* Gradient buttons */

.stApp button[kind="primary"],

.stApp [data-testid="stFormSubmitButton"] button {

    background: linear-gradient(

        90deg,

        #7544C8,

        #3478E5,

        #D65AAB

    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 11px !important;

    font-weight: 750 !important;

    transition: all 0.25s ease;

}
.stApp button[kind="primary"]:hover,

.stApp [data-testid="stFormSubmitButton"] button:hover {

    transform: translateY(-3px);

    box-shadow: 0 8px 20px rgba(80,55,160,0.25);
}
/* Quiz answer options */
.stApp [data-testid="stRadio"] {
    background: linear-gradient(
        110deg,
        #FFFFFF,
        #F5F0FF,
        #EFF5FF
    );
    border: 1px solid #DCCEF5;
    border-radius: 12px;
    padding: 12px 15px;
    margin-bottom: 15px;
    transition: all 0.25s ease;
}
.stApp [data-testid="stRadio"]:hover {
    border-color: #9875DA;
    box-shadow: 0 5px 14px rgba(80,55,160,0.13);
    transform: translateY(-2px);
}
.stApp [data-testid="stRadio"] label {
    font-weight: 600 !important;
    color: #354366 !important;
}
/* Answer explanation expanders */
.stApp [data-testid="stExpander"] {
    border: 1px solid #D5C5F2 !important;
    border-radius: 14px !important;
    background: rgba(255,255,255,0.45) !important;
    transition: all 0.25s ease;
}
.stApp [data-testid="stExpander"]:hover {
    border-color: #9875DA !important;
    box-shadow: 0 7px 17px rgba(80,55,160,0.13);
}
/* Feedback messages */
.stApp [data-testid="stAlert"] {
    border-radius: 12px !important;
}
/* Progress bar */
.stApp [data-testid="stProgressBar"] > div {
    background: #E6DDF5 !important;
    border-radius: 20px !important;
}
.stApp [data-testid="stProgressBar"] [role="progressbar"] > div {
    background: linear-gradient(
        90deg,
        #7544C8,
        #3478E5,
        #D65AAB
    ) !important;
    border-radius: 20px !important;
}
/* Accessibility */
@media (prefers-reduced-motion: reduce)*&#x20;{*
    .stApp [data-testid="stVerticalBlockBorderWrapper"],
    .stApp [data-testid="stRadio"],
    .stApp [data-testid="stExpander"],
    .stApp button {
        transition: none !important;
    }
}

/* Improve Practice Quiz font sizes */
/* Question headings */
.stApp [data-testid="stVerticalBlockBorderWrapper"] h3 {
    font-size: 24px !important;
    font-weight: 800 !important;
}

/* Question text */
.stApp [data-testid="stVerticalBlockBorderWrapper"] p {
    font-size: 17px !important;
    line-height: 1.7 !important;
}

/* Answer option text */
.stApp [data-testid="stRadio"] label,
.stApp [data-testid="stRadio"] label p {
    font-size: 16px !important;
    line-height: 1.6 !important;
    font-weight: 500 !important;
}

/* Answer instruction */
.stApp [data-testid="stCaptionContainer"] {
    font-size: 15px !important;
}

/* Radio option spacing */
.stApp [data-testid="stRadio"] {
    padding: 16px !important;
    margin-top: 10px !important;
    margin-bottom: 15px !important;
}

/* Expand the answer options area */
.stApp [data-testid="stRadio"] {
    width: 100% !important;
    max-width: 100% !important;
    display: block !important;
}

.stApp [data-testid="stRadio"] > div,
.stApp [data-testid="stRadio"] [role="radiogroup"] {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}

/* Make each answer row use the available width */
.stApp [data-testid="stRadio"] [role="radiogroup"] > label {
    width: 100% !important;
    box-sizing: border-box !important;
    padding: 8px 10px !important;
    border-radius: 8px !important;
}

/* Gentle answer hover */
.stApp [data-testid="stRadio"] [role="radiogroup"] > label:hover {
    background: #EDE5FF !important;
}


/* =================================
   PRACTICE QUIZ FORM READABILITY
================================= */

/* Form field labels */
.stSelectbox label,
.stTextInput label,
.stRadio > label,
.stNumberInput label {
    font-size: 17px !important;
    font-weight: 600 !important;
    color: #25345c !important;
}

/* Dropdown selected values */
.stSelectbox [data-baseweb="select"] div,
.stSelectbox [data-baseweb="select"] span {
    font-size: 17px !important;
}

/* Topic input text */
.stTextInput input {
    font-size: 17px !important;
    padding: 12px 14px !important;
}

/* Information and success messages */
.stAlert p {
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* Question headings */
.stMarkdown h3 {
    font-size: 23px !important;
    font-weight: 700 !important;
}

/* Question descriptions */
.stMarkdown p {
    font-size: 16px;
    line-height: 1.7;
}

/* Radio answer text */
.stRadio label p {
    font-size: 16px !important;
    line-height: 1.6 !important;
}

/* Form field spacing */
.stSelectbox,
.stTextInput,
.stRadio {
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)
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
    # Difficulty selection
    difficulty = st.selectbox(
        "🎯 Select quiz difficulty",
        ["Easy", "Medium", "Hard"],
        index=1,
        help="Choose how challenging your practice questions should be."
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

                def validate_generated_questions(generated_questions):

                    """Check that the generator returned five usable MCQs."""

                    if not isinstance(generated_questions, list):

                        raise ValueError("The quiz generator did not return a question list.")
                    if len(generated_questions) != 5:

                        raise ValueError(
                            f"Expected 5 questions, but received {len(generated_questions)}."
                        )
                    for number, question in enumerate(generated_questions, start=1):
                        if not isinstance(question, dict):
                            raise ValueError(f"Question {number} has an invalid format.")
                        required_keys = {"question", "options", "correct_answer", "explanation"}

                        missing_keys = required_keys - set(question.keys())
                        if missing_keys:
                            raise ValueError(
                                f"Question {number} is missing: {', '.join(sorted(missing_keys))}."
                            )
                        if not isinstance(question["question"], str) or not question["question"].strip():
                            raise ValueError(f"Question {number} has no question text.")
                        options = question["options"]
                        if not isinstance(options, dict) or set(options.keys()) != {"A", "B", "C", "D"}:
                            raise ValueError(
                                f"Question {number} must contain exactly options A, B, C and D."
                            )
                        if any(not isinstance(value, str) or not value.strip() for value in options.values()):
                            raise ValueError(f"Question {number} contains an empty answer option.")
                        if question["correct_answer"] not in {"A", "B", "C", "D"}:
                            raise ValueError(
                                f"Question {number} has an invalid correct-answer key."
                            )
                        if not isinstance(question["explanation"], dict):
                            raise ValueError(f"Question {number} has an invalid explanation.")
                    return generated_questions
                # Collect earlier questions so Gemini can try to avoid repeats.
                previous_questions = []
                if (
                    st.session_state.get("quiz_learner_id") == learner["id"]
                    and st.session_state.get("quiz_topic", "").strip().lower() == topic.strip().lower()
                    and st.session_state.get("quiz_type") == question_type
                ):
                    previous_questions = [
                        question.get("question", "")
                        for question in st.session_state.get("quiz_questions", [])
                        if isinstance(question, dict)
                    ]
                gemini_error_message = None
                questions = None
                quiz_mode = None

                # Try Gemini first.
                try:
                    with st.spinner("🤖 Gemini is creating your questions..."):
                        questions = generate_quiz(
                            subject=learner["subject"],
                            topic=topic.strip(),
                            level=learner["current_level"],
                            question_type=question_type,
                            difficulty=difficulty,
                            previous_questions=previous_questions
                        )
                    questions = validate_generated_questions(questions)

                    quiz_mode = "AI"
                except Exception as error:

                    gemini_error_message = str(error)
                # If Gemini fails or returns an invalid result, try the fixed demo set.

                if questions is None:

                    try:

                        with st.spinner("🧪 Loading backup practice questions..."):

                            demo_questions = generate_demo_quiz(

                                subject=learner["subject"],

                                topic=topic.strip(),

                                level=learner["current_level"],

                                question_type=question_type,

                                difficulty=difficulty
                            )
                        questions = validate_generated_questions(demo_questions)

                        quiz_mode = "Demo"
                    except Exception as demo_error:

                        st.error("Quiz generation could not be completed.")

                        st.error(f"Gemini issue: {gemini_error_message or 'No questions were returned.'}")

                        st.error(f"Demo issue: {demo_error}")

                        questions = None

                        quiz_mode = None
                if questions:

                    st.session_state["quiz_questions"] = questions

                    st.session_state["quiz_topic"] = topic.strip()

                    st.session_state["quiz_type"] = question_type

                    st.session_state["quiz_difficulty"] = difficulty

                    st.session_state["quiz_mode"] = quiz_mode

                    st.session_state["quiz_learner_id"] = learner["id"]
                    # Reset previous quiz results and radio selections.

                    st.session_state["quiz_submitted"] = False

                    st.session_state.pop("quiz_score", None)

                    st.session_state.pop("quiz_answers", None)

                    st.session_state["quiz_saved"] = False
                    for i in range(1, 6):
                        st.session_state.pop(f"question_{i}", None)
                    if quiz_mode == "AI":
                        st.success("🎉 Your five AI-generated questions are ready!")
                    else:
                        st.warning(
                            "⚠️ Gemini could not generate a valid quiz, so Demo Mode is active. "

                            "These are predefined questions and may not match your selected topic."
                        )
                        with st.expander("Why did Gemini generation fail?"):
                            st.code(gemini_error_message or "Gemini returned no usable questions.")

    # Display quiz outside Generate button
    if st.session_state.get("quiz_questions"):
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
        # Quiz Form
        with st.form("quiz_form"):
            for index, question in enumerate(
                st.session_state["quiz_questions"],
                start=1
            ):
                # Individual question card
                with st.container(border=True):
                    st.markdown(
                        f"### 📝 Question {index}"
                    )
                    st.markdown(
                        f"**{question['question']}**"
                    )
                    st.caption("Select one correct answer:")
                    selected_answer = st.radio(
                        f"Your answer for Question {index}",
                        options=["A", "B", "C", "D"],
                        index=None,
                        format_func=lambda option, q=question: (
                            f"{option}. {q['options'][option]}"
                        ),
                        key=f"question_{index}",
                        disabled=quiz_already_submitted,
                        width="stretch"
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
            ) * 100 if total_questions else 0

            incorrect_answers = total_questions - score

            st.divider()

            # Quiz Results Header
            st.subheader("🏆 Your Quiz Results")

            # Main Score Card
            with st.container(border=True):

                st.markdown("### 🎉 Your Performance")

                score_col, accuracy_col = st.columns(2)

                with score_col:
                    st.metric(
                        "🏆 Your Score",
                        f"{score}/{total_questions}"
                    )

                with accuracy_col:
                    st.metric(
                        "🎯 Accuracy",
                        f"{percentage:.0f}%"
                    )

                st.progress(percentage / 100)

                if percentage >= 80:
                    st.success(
                        "🌟 Excellent work! You have performed very well!"
                    )
                elif percentage >= 50:
                    st.info(
                        "👏 Good effort! Keep practising to improve further."
                    )
                else:
                    st.warning(
                        "💪 Keep learning! Review the explanations and try again."
                    )

            # Answer Statistics Cards
            st.write("### 📊 Answer Statistics")

            correct_col, incorrect_col, total_col = st.columns(3)

            with correct_col:
                with st.container(border=True):
                    st.metric(
                        "✅ Correct Answers",
                        score
                    )

            with incorrect_col:
                with st.container(border=True):
                    st.metric(
                        "❌ Incorrect Answers",
                        incorrect_answers
                    )

            with total_col:
                with st.container(border=True):
                    st.metric(
                        "📝 Total Questions",
                        total_questions
                    )

            # Quiz Mode Information
            if st.session_state.get("quiz_mode") == "Demo":

                st.info(
                    "🧪 This result came from a predefined demo quiz."
                )

            if st.session_state.get("quiz_saved", False):

                st.success(
                    "💾 Your quiz attempt has been saved successfully!"
                )

            st.divider()

            # Detailed Answer Review
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
                    f"📝 Question {index}: {question['question']}",
                    expanded=True
                ):

                    # Your Answer
                    if selected_answer is not None:
                        st.write(
                            f"**Your answer:** {selected_answer}. "
                            f"{question['options'][selected_answer]}"
                        )
                    else:
                        st.write("**Your answer:** Not answered")

                    # Correct Answer
                    st.write(
                        f"**Correct answer:** {correct_answer}. "
                        f"{correct_text}"
                    )

                    # Answer Status
                    if selected_answer == correct_answer:

                        st.success("✅ Correct answer!")

                    else:

                        st.error("❌ Incorrect answer!")

                    st.divider()

                    # Detailed Explanation
                    if st.session_state["quiz_type"] == "Theory":

                        display_theory_explanation(
                            question["explanation"]
                        )

                    else:

                        display_maths_explanation(
                            question["explanation"]
                        )
