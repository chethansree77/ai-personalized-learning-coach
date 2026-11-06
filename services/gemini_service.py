
import os
import time
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# Create Gemini client
def get_gemini_client():

    if not API_KEY:
        raise ValueError(
            "Gemini API key not found. Please check your .env file."
        )

    return genai.Client(api_key=API_KEY)


# Generate personalized study plan
def generate_study_plan(
    subject,
    learning_goal,
    current_level,
    target_days,
    daily_hours
):

    client = get_gemini_client()

    prompt = f"""
You are an expert personal learning coach.

Create a detailed personalized study plan using these learner details:

Subject: {subject}
Learning Goal: {learning_goal}
Current Level: {current_level}
Target Duration: {target_days} days
Daily Study Time: {daily_hours} hours

IMPORTANT FORMATTING RULES:

1. Generate exactly {target_days} study days.
2. Every day must start with this heading format:

   ## Day 1: Topic Name
   ## Day 2: Topic Name

3. Continue sequentially until Day {target_days}.
4. Never skip or repeat a day number.
5. Give each day its own separate heading.

Under each heading include:
- Learning Topic
- Learning Objectives
- Explanation
- Practice Activities
- Estimated Study Time

LEARNING REQUIREMENTS:

1. Start from the learner's current level.
2. Arrange topics from basic to advanced.
3. Use simple beginner-friendly language.
4. Include practical examples and exercises.
5. Include revision and assessment days.
6. Allocate realistic study time each day.
7. Support the learner's learning goal.
8. Cover the complete target duration.

Return only the organized day-wise study plan.
"""

    # Models to try in order
    models = [
        "gemini-3.5-flash-lite",
        "gemini-flash-lite-latest",
        "gemini-flash-latest"
    ]

    errors = []

    for model in models:

        # Retry each model up to two times
        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if not response.text:
                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                return response.text

            except Exception as error:

                error_message = str(error)

                errors.append(
                    f"{model}, attempt {attempt + 1}: {error_message}"
                )

                # Retry only temporary server errors
                temporary_error = any(
                    code in error_message
                    for code in ["503", "UNAVAILABLE", "500", "502", "504"]
                )

                if temporary_error and attempt == 0:
                    time.sleep(3)
                    continue

                # Do not retry authentication or other permanent errors
                break

    raise RuntimeError(
        "All Gemini model attempts failed. "
        "The service may be temporarily unavailable.\n\n"
        + "\n".join(errors)
    )
