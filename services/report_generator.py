
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)


def generate_progress_report(
    learner,
    study_plan,
    study_progress,
    quiz_history
):
    """Generate a downloadable PDF learning progress report."""

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
        title="AI Personalized Learning Progress Report"
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=21,
        textColor=colors.HexColor("#4338CA"),
        alignment=TA_CENTER,
        spaceAfter=10
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#4338CA"),
        spaceBefore=16,
        spaceAfter=8
    )

    normal_style = styles["BodyText"]

    story = []

    # Report title
    story.append(
        Paragraph("AI Personalized Learning Coach", title_style)
    )
    story.append(
        Paragraph("Learning Progress Report", styles["Heading2"])
    )
    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y')}",
            normal_style
        )
    )

    story.append(HRFlowable(
        width="100%",
        thickness=1,
        color=colors.HexColor("#C7D2FE"),
        spaceBefore=10,
        spaceAfter=10
    ))

    # Learner details
    story.append(Paragraph("1. Learner Details", heading_style))

    learner_data = [
        ["Field", "Details"],
        ["Subject", str(learner.get("subject", "N/A"))],
        ["Learning Goal", str(learner.get("learning_goal", "N/A"))],
        ["Current Level", str(learner.get("current_level", "N/A"))],
        ["Target Duration", f"{learner.get('target_days', 0)} days"],
        ["Daily Study Time", f"{learner.get('daily_hours', 0)} hours"]
    ]

    learner_table = Table(
        learner_data,
        colWidths=[150, 330]
    )

    learner_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4338CA")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#EEF2FF"))
    ]))

    story.append(learner_table)

    # Study progress
    story.append(Paragraph("2. Study Progress", heading_style))

    total_days = len(study_progress)
    completed_days = sum(
        1 for completed in study_progress.values() if completed
    )
    remaining_days = max(total_days - completed_days, 0)

    completion_percentage = (
        (completed_days / total_days) * 100
        if total_days else 0
    )

    progress_data = [
        ["Metric", "Result"],
        ["Total Study Days", str(total_days)],
        ["Completed Days", str(completed_days)],
        ["Remaining Days", str(remaining_days)],
        ["Completion Percentage", f"{completion_percentage:.1f}%"]
    ]

    progress_table = Table(
        progress_data,
        colWidths=[240, 240]
    )

    progress_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0891B2")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))

    story.append(progress_table)

    # Quiz performance
    story.append(Paragraph("3. Quiz Performance", heading_style))

    attempts = list(quiz_history)

    if attempts:
        total_score = sum(
            row["score"] for row in attempts
        )
        total_questions = sum(
            row["total_questions"] for row in attempts
        )

        average_accuracy = (
            (total_score / total_questions) * 100
            if total_questions else 0
        )

        best_accuracy = max(
            (
                row["score"] / row["total_questions"] * 100
                if row["total_questions"] else 0
            )
            for row in attempts
        )

        quiz_data = [
            ["Metric", "Result"],
            ["Total Quiz Attempts", str(len(attempts))],
            ["Average Accuracy", f"{average_accuracy:.1f}%"],
            ["Best Accuracy", f"{best_accuracy:.1f}%"]
        ]

        quiz_table = Table(
            quiz_data,
            colWidths=[240, 240]
        )

        quiz_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#059669")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ("PADDING", (0, 0), (-1, -1), 8)
        ]))

        story.append(quiz_table)

        story.append(Spacer(1, 10))
        story.append(Paragraph("Quiz History", styles["Heading3"]))

        history_data = [
            ["Topic", "Score", "Accuracy", "Mode"]
        ]

        for row in attempts:
            score = row["score"]
            total = row["total_questions"]

            accuracy = (
                (score / total) * 100
                if total else 0
            )

            history_data.append([
                Paragraph(str(row["topic"]), normal_style),
                f"{score}/{total}",
                f"{accuracy:.1f}%",
                str(row["quiz_mode"])
            ])

        history_table = Table(
            history_data,
            colWidths=[210, 65, 85, 120],
            repeatRows=1
        )

        history_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ("PADDING", (0, 0), (-1, -1), 7),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        story.append(history_table)

    else:
        story.append(
            Paragraph(
                "No quiz attempts recorded yet.",
                normal_style
            )
        )

    # Footer message
    story.append(Spacer(1, 20))
    story.append(HRFlowable(
        width="100%",
        thickness=1,
        color=colors.HexColor("#C7D2FE")
    ))
    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "Keep learning, keep practicing, and keep improving!",
            ParagraphStyle(
                "Footer",
                parent=normal_style,
                alignment=TA_CENTER,
                textColor=colors.HexColor("#4338CA"),
                fontSize=11
            )
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()
