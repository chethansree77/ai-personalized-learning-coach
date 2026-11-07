
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


IST = ZoneInfo("Asia/Kolkata")


def _convert_utc_to_ist(value):
    """Convert SQLite's UTC timestamp text into readable Indian Standard Time."""
    if not value:
        return value

    try:
        timestamp = datetime.fromisoformat(str(value))
        # SQLite CURRENT_TIMESTAMP stores UTC as a timezone-naive string.
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp.astimezone(IST).strftime("%Y-%m-%d %H:%M:%S IST")
    except (TypeError, ValueError):
        # Preserve unexpected timestamp formats rather than breaking the page.
        return value


def _convert_record_timestamps(record):
    """Return a dictionary with timestamp columns displayed in IST."""
    result = dict(record)
    for field in ("created_at", "completed_at"):
        if field in result and result[field]:
            result[field] = _convert_utc_to_ist(result[field])
    return result


# Database file location
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "learning_coach.db"


# Connect to SQLite database
def get_connection():

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


# Create learner profile table
def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            learning_goal TEXT NOT NULL,
            current_level TEXT NOT NULL,
            target_days INTEGER NOT NULL,
            daily_hours REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()



# Save or update learner profile without creating duplicate subjects
def save_learner(
    subject,
    learning_goal,
    current_level,
    target_days,
    daily_hours
):

    connection = get_connection()
    cursor = connection.cursor()

    # Find the latest existing profile for this subject
    cursor.execute("""
        SELECT id
        FROM learners
        WHERE LOWER(TRIM(subject)) = LOWER(TRIM(?))
        ORDER BY id DESC
        LIMIT 1
    """, (subject,))

    existing_learner = cursor.fetchone()

    if existing_learner:

        learner_id = existing_learner["id"]

        # Update the existing profile and preserve its learner ID
        cursor.execute("""
            UPDATE learners
            SET subject = ?,
                learning_goal = ?,
                current_level = ?,
                target_days = ?,
                daily_hours = ?
            WHERE id = ?
        """, (
            subject,
            learning_goal,
            current_level,
            target_days,
            daily_hours,
            learner_id
        ))

    else:

        # Create a new profile only if the subject does not exist
        cursor.execute("""
            INSERT INTO learners (
                subject,
                learning_goal,
                current_level,
                target_days,
                daily_hours
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            subject,
            learning_goal,
            current_level,
            target_days,
            daily_hours
        ))

        learner_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return learner_id



# Get latest learner profile
def get_latest_learner():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM learners
        ORDER BY id DESC
        LIMIT 1
    """)

    learner = cursor.fetchone()
    connection.close()

    if learner is None:
        return None

    return _convert_record_timestamps(learner)


# Get all learner profiles
def get_all_learners():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM learners
        ORDER BY id DESC
    """)

    learners = cursor.fetchall()
    connection.close()

    return [_convert_record_timestamps(learner) for learner in learners]


# Save generated study plan
def save_study_plan(learner_id, plan_text):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            plan_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        )
    """)

    cursor.execute("""
        INSERT INTO study_plans (learner_id, plan_text)
        VALUES (?, ?)
    """, (learner_id, plan_text))

    connection.commit()
    plan_id = cursor.lastrowid
    connection.close()

    return plan_id


# Get latest saved study plan
def get_latest_study_plan(learner_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM study_plans
        WHERE learner_id = ?
        ORDER BY id DESC
        LIMIT 1
    """, (learner_id,))

    plan = cursor.fetchone()
    connection.close()

    if plan is None:
        return None

    return _convert_record_timestamps(plan)


# Create study progress table
def create_study_progress_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            plan_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            plan_id INTEGER NOT NULL,
            day_number INTEGER NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            completed_at TIMESTAMP,
            UNIQUE(plan_id, day_number),
            FOREIGN KEY (learner_id) REFERENCES learners(id),
            FOREIGN KEY (plan_id) REFERENCES study_plans(id)
        )
    """)

    connection.commit()
    connection.close()


# Get completed study days for a plan
def get_study_progress(plan_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT day_number, completed
        FROM study_progress
        WHERE plan_id = ?
    """, (plan_id,))

    rows = cursor.fetchall()
    connection.close()

    return {
        row["day_number"]: bool(row["completed"])
        for row in rows
    }


# Save or update study day completion
def set_study_day_completion(
    learner_id,
    plan_id,
    day_number,
    completed
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO study_progress (
            learner_id,
            plan_id,
            day_number,
            completed,
            completed_at
        )
        VALUES (
            ?, ?, ?, ?,
            CASE WHEN ? = 1 THEN CURRENT_TIMESTAMP ELSE NULL END
        )
        ON CONFLICT(plan_id, day_number)
        DO UPDATE SET
            completed = excluded.completed,
            completed_at = excluded.completed_at
    """, (
        learner_id,
        plan_id,
        day_number,
        int(completed),
        int(completed)
    ))

    connection.commit()
    connection.close()


# Create quiz attempts table and update old databases
def create_quiz_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            answers TEXT,
            quiz_mode TEXT DEFAULT 'AI',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        )
    """)

    cursor.execute("PRAGMA table_info(quiz_attempts)")

    columns = [
        row["name"] for row in cursor.fetchall()
    ]

    if "quiz_mode" not in columns:

        cursor.execute("""
            ALTER TABLE quiz_attempts
            ADD COLUMN quiz_mode TEXT DEFAULT 'AI'
        """)

    connection.commit()
    connection.close()


# Save quiz attempt
def save_quiz_attempt(
    learner_id,
    topic,
    score,
    total_questions,
    answers,
    quiz_mode="AI"
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO quiz_attempts (
            learner_id,
            topic,
            score,
            total_questions,
            answers,
            quiz_mode
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        learner_id,
        topic,
        score,
        total_questions,
        json.dumps(answers),
        quiz_mode
    ))

    connection.commit()
    attempt_id = cursor.lastrowid
    connection.close()

    return attempt_id


# Get quiz history
def get_quiz_history(learner_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Ensure quiz table exists
    create_cursor = cursor

    create_cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            learner_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            answers TEXT,
            quiz_mode TEXT DEFAULT 'AI',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (learner_id) REFERENCES learners(id)
        )
    """)

    create_cursor.execute("PRAGMA table_info(quiz_attempts)")

    columns = [
        row["name"] for row in create_cursor.fetchall()
    ]

    if "quiz_mode" not in columns:

        create_cursor.execute("""
            ALTER TABLE quiz_attempts
            ADD COLUMN quiz_mode TEXT DEFAULT 'AI'
        """)

    cursor.execute("""
        SELECT
            id,
            topic,
            score,
            total_questions,
            answers,
            created_at,
            COALESCE(quiz_mode, 'AI') AS quiz_mode
        FROM quiz_attempts
        WHERE learner_id = ?
        ORDER BY id DESC
    """, (learner_id,))

    history = cursor.fetchall()

    connection.commit()
    connection.close()

    return [_convert_record_timestamps(attempt) for attempt in history]
