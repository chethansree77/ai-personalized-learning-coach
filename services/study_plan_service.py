
from services.gemini_service import generate_study_plan


def create_personalized_plan(learner):
    """
    Generate a personalized study plan
    using the saved learner information.
    """

    plan = generate_study_plan(
        subject=learner["subject"],
        learning_goal=learner["learning_goal"],
        current_level=learner["current_level"],
        target_days=learner["target_days"],
        daily_hours=learner["daily_hours"]
    )

    if not plan or not plan.strip():
        raise ValueError("The AI generated an empty study plan.")

    return plan
