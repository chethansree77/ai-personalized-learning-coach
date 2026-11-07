
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


# --------------------------------------------------
# Configure page
# --------------------------------------------------

st.set_page_config(
    page_title="Personalized Study Plan",
    page_icon="📅",
    layout="wide"
)


# --------------------------------------------------
# Page styling
# --------------------------------------------------

st.markdown("""
<style>

/* Page background */
.stApp {
    background: linear-gradient(
        135deg,
        #F5EEFF,
        #EEF5FF,
        #FFF0F7
    );
}

/* Page heading */
h1 {
    color: #5836A3 !important;
    font-size: 36px !important;
    font-weight: 800 !important;
}

/* Section headings */
h2, h3 {
    color: #5836A3 !important;
    font-weight: 700 !important;
}

/* Labels */
.stApp label {
    font-size: 16px !important;
    font-weight: 600 !important;
}

/* General bordered cards */
.stApp [data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(
        120deg,
        #EAE2FF,
        #E3EDFF,
        #FFE7F2
    ) !important;

    border: 1px solid #CBB8F0 !important;
    border-radius: 18px !important;

    box-shadow: 0 6px 18px rgba(80, 55, 160, 0.13);

    transition: all 0.3s ease;
}

/* General card hover */
.stApp [data-testid="stVerticalBlockBorderWrapper"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 11px 24px rgba(80, 55, 160, 0.20);
}

/* Primary buttons */
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

    font-size: 16px !important;
    font-weight: 700 !important;

    transition: all 0.25s ease;
}

.stApp button[kind="primary"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(80, 55, 160, 0.25);
}

/* Sidebar */
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

[data-testid="stSidebarNav"] a {
    color: white !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.25) !important;
    border-left: 4px solid #FFE5B4 !important;
}

/* General text readability */
.stApp p {
    font-size: 16px !important;
    line-height: 1.65 !important;
}

/* Progress bar */
.stApp [data-testid="stProgressBar"] {
    background: transparent !important;
    padding: 5px 0 !important;
}

.stApp [data-testid="stProgressBar"] > div {
    background: #E5DDF5 !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    height: 15px !important;
}

.stApp [data-testid="stProgressBar"] [role="progressbar"] > div {
    background: linear-gradient(
        90deg,
        #7544C8,
        #3478E5,
        #D65AAB
    ) !important;

    border-radius: 20px !important;
    height: 15px !important;

    box-shadow: 0 2px 9px rgba(117, 68, 200, 0.30);

    transition: width 0.8s ease-in-out;
}

/* Daily Progress checklist cards */
.stApp [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]) {
    width: 100% !important;
}

.stApp [data-testid="stCheckbox"] {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;

    background: linear-gradient(
        110deg,
        #FFFFFF,
        #F2EDFF,
        #EDF4FF
    ) !important;

    border: 1px solid #D8C9F2 !important;
    border-radius: 14px !important;

    padding: 15px 18px !important;
    margin-bottom: 12px !important;

    box-shadow: 0 3px 10px rgba(80, 55, 160, 0.09);

    transition: transform 0.25s ease,
                box-shadow 0.25s ease,
                border-color 0.25s ease;
}

.stApp [data-testid="stCheckbox"]:hover {
    transform: translateY(-3px);
    border-color: #9672D8 !important;

    box-shadow: 0 8px 18px rgba(80, 55, 160, 0.17);
}

.stApp [data-testid="stCheckbox"] > label {
    width: 100% !important;
    display: flex !important;
    align-items: center !important;
}

.stApp [data-testid="stCheckbox"] label p {
    flex: 1 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    line-height: 1.7 !important;
    color: #394567 !important;
}

/* Completed checklist day */
.stApp [data-testid="stCheckbox"]:has(input:checked) {
    background: linear-gradient(
        110deg,
        #E0F7E9,
        #D5F5E5,
        #E8FFF1
    ) !important;

    border: 1px solid #82C99B !important;
    box-shadow: 0 4px 12px rgba(46, 139, 87, 0.12);
}

.stApp [data-testid="stCheckbox"]:has(input:checked):hover {
    border-color: #36A269 !important;
    box-shadow: 0 8px 18px rgba(46, 139, 87, 0.20);
}

/* Study Progress metric cards */
.stApp [data-testid="stMetric"] {
    background: linear-gradient(
        135deg,
        #F0E7FF,
        #E7EFFF
    );

    border: 1px solid #D3C2F3;
    border-radius: 16px;

    padding: 18px 20px;

    box-shadow: 0 4px 12px rgba(80, 55, 160, 0.10);

    transition: transform 0.25s ease,
                box-shadow 0.25s ease;
}

.stApp [data-testid="stMetric"]:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 9px 20px rgba(80, 55, 160, 0.18);
}

.stApp [data-testid="stMetricLabel"] {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #5836A3 !important;
}

.stApp [data-testid="stMetricValue"] {
    font-size: 30px !important;
    font-weight: 800 !important;
    color: #3478E5 !important;
}

/* Roadmap typography */
.stApp [data-testid="stMarkdownContainer"] h1,
.stApp [data-testid="stMarkdownContainer"] h2,
.stApp [data-testid="stMarkdownContainer"] h3 {
    color: #5836A3 !important;
    font-weight: 800 !important;
    margin-top: 22px !important;
    margin-bottom: 12px !important;
}

.stApp [data-testid="stMarkdownContainer"] p {
    color: #394567 !important;
    line-height: 1.8 !important;
    margin-bottom: 12px !important;
}

.stApp [data-testid="stMarkdownContainer"] ul,
.stApp [data-testid="stMarkdownContainer"] ol {
    padding-left: 28px !important;
    line-height: 1.9 !important;
}

.stApp [data-testid="stMarkdownContainer"] li {
    padding: 5px 0 !important;
    color: #394567 !important;
}

.stApp [data-testid="stMarkdownContainer"] hr {
    border-color: #D8C9F2 !important;
    margin: 20px 0 !important;
}

/* Individual roadmap cards */
.stApp [class*="st-key-roadmap_day_"] {
    border: 1px solid #D8C9F2 !important;
    border-radius: 16px !important;

    box-shadow: 0 4px 12px rgba(80, 55, 160, 0.10) !important;

    transition: transform 0.3s ease,
                box-shadow 0.3s ease,
                border-color 0.3s ease !important;
}

.stApp [class*="st-key-roadmap_day_"]:hover {
    transform: translateY(-5px) !important;
    border-color: #7544C8 !important;

    box-shadow: 0 12px 26px rgba(80, 55, 160, 0.25) !important;
}

/* Roadmap information labels */
.roadmap-label {
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
    display: inline-block;
    margin-right: 4px;
}

.topic-label {
    color: #7544C8;
    background: #EDE3FF;
}

.objectives-label {
    color: #2468C7;
    background: #E1EDFF;
}

.explanation-label {
    color: #16836F;
    background: #DDF7EF;
}

.practice-label {
    color: #C04491;
    background: #FCE5F3;
}

.time-label {
    color: #B66A13;
    background: #FFF0D9;
}

/* Roadmap completion indicators */
/* Compact roadmap status badge */
.roadmap-status {
    display: inline-block;
    padding: 3px 9px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: 0.2px;
}

.roadmap-completed {
    color: #187A45;
    background: #DDF7E7;
    border: 1px solid #82C99B;
}

.roadmap-pending {
    color: #6741B8;
    background: #EDE3FF;
    border: 1px solid #CBB8F0;
}

/* Reduced motion accessibility */
@media (prefers-reduced-motion: reduce) {
    .stApp [data-testid="stVerticalBlockBorderWrapper"],
    .stApp [data-testid="stCheckbox"],
    .stApp [data-testid="stMetric"],
    .stApp [class*="st-key-roadmap_day_"],
    .stApp button[kind="primary"],
    .stApp [data-testid="stProgressBar"] > div > div {
        transition: none !important;
    }
}

/* Force all sidebar navigation text to white */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a *,
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span,
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] p {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Sidebar navigation hover */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background: rgba(255, 255, 255, 0.20) !important;
    border-radius: 8px !important;
}

/* Active page */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.30) !important;
    border-left: 4px solid #FFE082 !important;
    border-radius: 8px !important;
}

/* Sidebar icons */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] svg {
    color: #FFFFFF !important;
}

/* Sidebar collapse and expand buttons */
/*[data-testid="stSidebarCollapseButton"] button,
[data-testid="stSidebarExpandButton"] button {
    background: linear-gradient(135deg, #7041C7, #3478E5) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 10px !important;
    color: white !important;
    transition: all 0.3s ease !important;*/
}

/* Arrow icon */
/*[data-testid="stSidebarCollapseButton"] button svg,
[data-testid="stSidebarExpandButton"] button svg {
    color: white !important;
    fill: white !important;
}*/

/* Hover effect */
/*[data-testid="stSidebarCollapseButton"] button:hover,
[data-testid="stSidebarExpandButton"] button:hover {
    background: linear-gradient(135deg, #D94FAE, #7041C7) !important;
    box-shadow: 0 4px 12px rgba(112, 65, 199, 0.3) !important;
    transform: scale(1.08);
}*/

/* Sidebar open and close buttons */
[data-testid="stSidebar"] button,
[data-testid="collapsedControl"] button,
button[data-testid="stSidebarCollapseButton"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Make navigation arrows white */
[data-testid="stSidebar"] button svg,
[data-testid="collapsedControl"] svg,
button[data-testid="stSidebarCollapseButton"] svg {
    color: #ffffff !important;
    fill: #ffffff !important;
    stroke: #ffffff !important;
}

/* Remove hover box and keep white arrow */
[data-testid="stSidebar"] button:hover,
[data-testid="collapsedControl"] button:hover,
button[data-testid="stSidebarCollapseButton"]:hover {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Save checkbox changes to SQLite
# --------------------------------------------------

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


# --------------------------------------------------
# Extract day headings
# --------------------------------------------------

def extract_study_days(plan_text):

    pattern = re.compile(
        r"^\s*(?:[-*]\s*)?(?:#{1,6}\s*)?"
        r"(?:\*\*)?Day\s+(\d+)\s*:\s*(.*?)"
        r"(?:\*\*)?\s*$",
        re.IGNORECASE | re.MULTILINE
    )

    days = {}

    for match in pattern.finditer(plan_text):

        day_number = int(match.group(1))
        topic = match.group(2).strip().rstrip("*").strip()

        if day_number not in days:
            days[day_number] = topic

    return sorted(days.items())


# --------------------------------------------------
# Page heading
# --------------------------------------------------

st.title("📅 Your Personalized Study Plan")

st.write(
    "Generate a customized learning schedule "
    "based on your subject, goals and available study time."
)

st.divider()


# --------------------------------------------------
# Retrieve learner profiles
# --------------------------------------------------

learners = get_all_learners()

if not learners:

    st.warning(
        "No learner profile found. "
        "Please complete Learner Setup first."
    )

    st.stop()


# Keep the latest profile for each subject
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
# Subject Selection Card
# --------------------------------------------------

with st.container(border=True):

    st.subheader("📚 Select Your Learning Subject")

    subject_options = list(learners_by_subject.keys())

    selected_subject = st.selectbox(
        "Choose the subject you want to study:",
        options=subject_options,
        format_func=lambda subject: learners_by_subject[subject]["subject"],
        key="study_plan_subject_selector"
    )


learner = learners_by_subject[selected_subject]


# --------------------------------------------------
# Create progress table
# --------------------------------------------------

create_study_progress_table()


# --------------------------------------------------
# Learning Profile Card
# --------------------------------------------------

with st.container(border=True):

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


# --------------------------------------------------
# Generate personalized study plan
# --------------------------------------------------

with st.container(border=True):

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


# --------------------------------------------------
# Display saved study plan
# --------------------------------------------------

saved_plan = get_latest_study_plan(learner["id"])

if saved_plan is not None:

    st.divider()

    plan_id = saved_plan["id"]

    # Read saved progress from SQLite
    progress = get_study_progress(plan_id)

    # Extract day headings
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

        # Study Progress Summary Card
        with st.container(border=True):

            st.subheader("📊 Your Study Progress")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📅 Total Study Days",
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

        st.divider()

        # Daily Progress Card
        with st.container(border=True):

            st.subheader("☑️ Mark Your Daily Progress")

            st.write(
                "Tick the checkbox after completing that day's "
                "learning activities. Your progress will be saved automatically."
            )

            # Display checkbox for every study day
            for day_number, topic in study_days:

                widget_key = (
                    f"study_plan_{plan_id}_day_{day_number}"
                )

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

        # Completion messages
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

    # --------------------------------------------------
    # Saved Learning Roadmap Card
    # --------------------------------------------------

    with st.container(border=True):

        st.subheader("📅 Your Saved Learning Roadmap")

        plan_text = saved_plan["plan_text"]

        # Split roadmap at each Day heading
        day_pattern = re.compile(
            r"(?=^\s*(?:[-*]\s*)?(?:#{1,6}\s*)?(?:\*\*)?Day\s+\d+\s*:)",
            re.IGNORECASE | re.MULTILINE
        )

        roadmap_sections = [
            section.strip()
            for section in day_pattern.split(plan_text)
            if section.strip()
        ]

        # Display each day with completion status
        for day_index, section in enumerate(roadmap_sections):

            day_match = re.match(
                r"^\s*(?:[-*]\s*)?(?:#{1,6}\s*)?(?:\*\*)?Day\s+(\d+)\s*:",
                section,
                re.IGNORECASE
            )

            if day_match:

                day_number = int(day_match.group(1))

                is_completed = progress.get(
                    day_number,
                    False
                )

                if is_completed:

                    status_html = (
                        '<div class="roadmap-status roadmap-completed">'
                        '✓ Completed'
                        '</div>'
                    )

                else:

                    status_html = (
                        '<div class="roadmap-status roadmap-pending">'
                        '○ Pending'
                        '</div>'
                    )

                # Individual roadmap day card
                with st.container(
                    border=True,
                    key=f"roadmap_day_{day_index}"
                ):

                    # Display completion status
                    st.markdown(
                        status_html,
                        unsafe_allow_html=True
                    )

                    styled_section = section

                    # Colored roadmap labels
                    label_styles = {
                        "Learning Topic": "topic-label",
                        "Learning Objectives": "objectives-label",
                        "Explanation": "explanation-label",
                        "Practice Activities": "practice-label",
                        "Estimated Study Time": "time-label"
                    }

                    for label, css_class in label_styles.items():

                        styled_section = re.sub(
                            rf"(^\s*[-*]\s*)({re.escape(label)}:)",
                            rf'\1<span class="roadmap-label {css_class}">\2</span>',
                            styled_section,
                            flags=re.IGNORECASE | re.MULTILINE
                        )

                    # Display roadmap content
                    st.markdown(
                        styled_section,
                        unsafe_allow_html=True
                    )

            else:

                # Preserve introductory roadmap content
                st.markdown(section)

else:

    st.info(
        f"No saved study plan found for {learner['subject']}. "
        "Generate your plan first."
    )
