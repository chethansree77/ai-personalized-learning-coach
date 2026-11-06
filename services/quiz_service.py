
import json
import re
import time

from services.gemini_service import get_gemini_client


# Models are attempted in order.
GEMINI_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-flash-latest"
]

MAX_RETRIES = 2
RETRY_DELAY = 3


def is_temporary_error(error):
    """Identify errors that may resolve after retrying."""

    error_text = str(error).lower()

    temporary_errors = [
        "503",
        "unavailable",
        "high demand",
        "500",
        "502",
        "504",
        "429",
        "resource_exhausted",
        "rate limit",
        "deadline exceeded"
    ]

    return any(
        message in error_text
        for message in temporary_errors
    )


def generate_quiz(subject, topic, level, question_type):

    client = get_gemini_client()

    if question_type == "Maths / Aptitude":

        explanation_instructions = """
        Create a structured MATHS / APTITUDE explanation.

        Return these fields:

        "formula": The main formula used. If no formula is needed, use "Not required".
        "symbols": Explain every symbol and mathematical value.
        "given_values": List the values provided in the question.
        "steps": A list of detailed calculation steps in the correct order.
        "reasoning": Explain why this method works in simple language.
        "shortcut": Give a shortcut method if useful. Otherwise explain that no shortcut is needed.
        "final_answer": State the correct answer clearly.
        "memory_tip": Give a short tip to remember the method.

        IMPORTANT:
        - Never skip calculation steps.
        - Use the exact values from the question.
        - Make the solution suitable for a beginner.
        - Check the calculation before returning the answer.
        """

        explanation_format = """
        "explanation": {
            "formula": "Formula here",
            "symbols": ["Meaning of each symbol"],
            "given_values": ["Values from the question"],
            "steps": ["Step 1", "Step 2", "Step 3"],
            "reasoning": "Simple explanation",
            "shortcut": "Shortcut method or Not required",
            "final_answer": "Final answer",
            "memory_tip": "Short memory tip"
        }
        """

    else:

        explanation_instructions = """
        Create a structured THEORY explanation.

        Return these fields:

        "concept": Explain the correct answer in simple language.
        "key_points": A list of important points.
        "example": Give a practical example where useful.
        "option_analysis": Explain why each incorrect option is wrong.
        "memory_tip": Give a short examination memory tip.

        IMPORTANT:
        - Use beginner-friendly language.
        - Explain the concept, not just the answer.
        - Keep the explanation clear and useful.
        """

        explanation_format = """
        "explanation": {
            "concept": "Simple concept explanation",
            "key_points": ["Important point 1", "Important point 2"],
            "example": "Practical example",
            "option_analysis": {
                "A": "Explanation",
                "B": "Explanation",
                "C": "Explanation",
                "D": "Explanation"
            },
            "memory_tip": "Short memory tip"
        }
        """

    prompt = f"""
    You are an expert personal learning coach and tutor.

    Create exactly 5 multiple-choice questions.

    Subject: {subject}
    Topic: {topic}
    Learner Level: {level}
    Question Type: {question_type}

    QUESTION REQUIREMENTS:

    1. Create exactly five relevant questions.
    2. Each question must have exactly four options.
    3. Each question must have exactly one correct answer.
    4. Avoid confusing or ambiguous questions.
    5. Use simple language appropriate for the learner.
    6. Do not reveal correct answers in the question.
    7. Do not include images in the question data.
    8. Verify that each correct answer matches its explanation.

    EXPLANATION REQUIREMENTS:

    {explanation_instructions}

    Return ONLY valid JSON in this format:

    {{
        "questions": [
            {{
                "question": "Question text",
                "options": {{
                    "A": "Option A",
                    "B": "Option B",
                    "C": "Option C",
                    "D": "Option D"
                }},
                "correct_answer": "A",
                {explanation_format}
            }}
        ]
    }}
    """

    response = None
    last_error = None

    # Try alternative Gemini models if one is unavailable.
    for model in GEMINI_MODELS:

        for attempt in range(MAX_RETRIES):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if not response.text:
                    raise ValueError(
                        "Gemini returned an empty response."
                    )

                break

            except Exception as error:

                last_error = error

                if is_temporary_error(error):

                    if attempt < MAX_RETRIES - 1:
                        time.sleep(RETRY_DELAY)
                        continue

                    # Move to the next model.
                    break

                # Do not repeatedly retry permanent errors.
                break

        if response is not None and response.text:
            break

    if response is None or not response.text:

        if last_error and is_temporary_error(last_error):

            raise RuntimeError(
                "Gemini is currently experiencing high demand. "
                "We tried multiple models, but none responded. "
                "Please wait a little and try again."
            ) from last_error

        raise RuntimeError(
            f"Unable to generate the quiz. Please check your "
            f"Gemini API configuration and try again. "
            f"Details: {last_error}"
        ) from last_error

    try:

        result_text = response.text.strip()

        result_text = re.sub(
            r"^```(?:json)?\s*|\s*```$",
            "",
            result_text
        )

        quiz_data = json.loads(result_text)

        questions = quiz_data.get("questions")

        if not isinstance(questions, list) or len(questions) != 5:
            raise ValueError(
                "The AI must generate exactly 5 questions."
            )

        for question in questions:

            required_keys = [
                "question",
                "options",
                "correct_answer",
                "explanation"
            ]

            if not all(key in question for key in required_keys):
                raise ValueError(
                    "A question is missing required information."
                )

            if not isinstance(question["options"], dict):
                raise ValueError(
                    "Question options must be an object."
                )

            if set(question["options"].keys()) != {
                "A", "B", "C", "D"
            }:
                raise ValueError(
                    "Each question must have exactly four options."
                )

            if question["correct_answer"] not in [
                "A", "B", "C", "D"
            ]:
                raise ValueError("Invalid correct answer.")

            explanation = question["explanation"]

            if not isinstance(explanation, dict):
                raise ValueError(
                    "Explanation must be structured data."
                )

            if question_type == "Maths / Aptitude":

                required_explanation_fields = [
                    "formula",
                    "symbols",
                    "given_values",
                    "steps",
                    "reasoning",
                    "shortcut",
                    "final_answer",
                    "memory_tip"
                ]

            else:

                required_explanation_fields = [
                    "concept",
                    "key_points",
                    "example",
                    "option_analysis",
                    "memory_tip"
                ]

            if not all(
                field in explanation
                for field in required_explanation_fields
            ):
                raise ValueError(
                    "The explanation is missing required sections."
                )

            if not str(explanation["memory_tip"]).strip():
                raise ValueError("Memory tip is empty.")

        return questions

    except Exception as error:

        raise RuntimeError(
            f"Quiz response validation failed: {error}"
        ) from error
