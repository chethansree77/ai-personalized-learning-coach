
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
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

    cell_style = ParagraphStyle(
        "TableCell",
        parent=normal_style,
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.black,
        wordWrap="CJK"
    )

    header_style = ParagraphStyle(
        "TableHeader",
        parent=cell_style,
        textColor=colors.white,
        fontName="Helvetica-Bold"
    )

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

    # 1. Learner Details
    story.append(
        Paragraph("1. Learner Details", heading_style)
    )

    learner_data = [
        [
            Paragraph("Field", header_style),
            Paragraph("Details", header_style)
        ],
        [
            Paragraph("Subject", cell_style),
            Paragraph(
                escape(str(learner.get("subject", "N/A"))),
                cell_style
            )
        ],
        [
            Paragraph("Learning Goal", cell_style),
            Paragraph(
                escape(str(learner.get("learning_goal", "N/A"))),
                cell_style
            )
        ],
        [
            Paragraph("Current Level", cell_style),
            Paragraph(
                escape(str(learner.get("current_level", "N/A"))),
                cell_style
            )
        ],
        [
            Paragraph("Target Duration", cell_style),
            Paragraph(
                f"{learner.get('target_days', 0)} days",
                cell_style
            )
        ],
        [
            Paragraph("Daily Study Time", cell_style),
            Paragraph(
                f"{learner.get('daily_hours', 0)} hours",
                cell_style
            )
        ]
    ]

    learner_table = Table(
        learner_data,
        colWidths=[150, 330],
        repeatRows=1
    )

    learner_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4338CA")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 1), (0, -1), colors.HexColor("#EEF2FF"))
    ]))

    story.append(learner_table)

    # 2. Study Progress
    story.append(
        Paragraph("2. Study Progress", heading_style)
    )

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
        [
            Paragraph("Metric", header_style),
            Paragraph("Result", header_style)
        ],
        [
            Paragraph("Total Study Days", cell_style),
            Paragraph(str(total_days), cell_style)
        ],
        [
            Paragraph("Completed Days", cell_style),
            Paragraph(str(completed_days), cell_style)
        ],
        [
            Paragraph("Remaining Days", cell_style),
            Paragraph(str(remaining_days), cell_style)
        ],
        [
            Paragraph("Completion Percentage", cell_style),
            Paragraph(f"{completion_percentage:.1f}%", cell_style)
        ]
    ]

    progress_table = Table(
        progress_data,
        colWidths=[240, 240]
    )

    progress_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0891B2")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))

    story.append(progress_table)

    # 3. Quiz Performance
    story.append(
        Paragraph("3. Quiz Performance", heading_style)
    )

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
            [
                Paragraph("Metric", header_style),
                Paragraph("Result", header_style)
            ],
            [
                Paragraph("Total Quiz Attempts", cell_style),
                Paragraph(str(len(attempts)), cell_style)
            ],
            [
                Paragraph("Average Accuracy", cell_style),
                Paragraph(f"{average_accuracy:.1f}%", cell_style)
            ],
            [
                Paragraph("Best Accuracy", cell_style),
                Paragraph(f"{best_accuracy:.1f}%", cell_style)
            ]
        ]

        quiz_table = Table(
            quiz_data,
            colWidths=[240, 240]
        )

        quiz_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#059669")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP")
        ]))

        story.append(quiz_table)

        story.append(Spacer(1, 10))

        story.append(
            Paragraph("Quiz History", styles["Heading3"])
        )

        history_data = [
            [
                Paragraph("Topic", header_style),
                Paragraph("Score", header_style),
                Paragraph("Accuracy", header_style),
                Paragraph("Mode", header_style)
            ]
        ]

        for row in attempts:

            score = row["score"]
            total = row["total_questions"]

            accuracy = (
                (score / total) * 100
                if total else 0
            )

            history_data.append([
                Paragraph(
                    escape(str(row["topic"])),
                    cell_style
                ),
                Paragraph(f"{score}/{total}", cell_style),
                Paragraph(f"{accuracy:.1f}%", cell_style),
                Paragraph(
                    escape(str(row["quiz_mode"])),
                    cell_style
                )
            ])

        history_table = Table(
            history_data,
            colWidths=[210, 65, 85, 120],
            repeatRows=1
        )

        history_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
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
