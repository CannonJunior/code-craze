"""
Seed database with sample questions and test data.

This script loads sample questions from JSON and creates a test user
for trying out the application.
"""

import json
from pathlib import Path
from sqlalchemy.orm import Session

from backend.database.db import SessionLocal, init_db
from backend.database.models import User, Question, UserPreference, Badge


def load_sample_questions(db: Session):
    """
    Load sample questions from JSON file.

    Args:
        db: Database session.
    """
    # Path to sample questions
    questions_file = Path(__file__).parent.parent.parent / "content" / "questions" / "sample_questions.json"

    if not questions_file.exists():
        print(f"❌ Sample questions file not found: {questions_file}")
        return

    # Load JSON
    with open(questions_file, 'r') as f:
        data = json.load(f)

    # Clear existing questions
    db.query(Question).delete()

    # Add questions
    for q_data in data.get("questions", []):
        question = Question(
            id=q_data["id"],
            question_text=q_data["question_text"],
            question_type=q_data["question_type"],
            topic_id=q_data["topic_id"],
            difficulty=q_data["difficulty"],
            answers=q_data["answers"],
            solution_steps=q_data.get("solution_steps"),
            code_snippet=q_data.get("code_snippet"),
            lesson_reference=q_data.get("lesson_reference"),
            image_url=q_data.get("image_url")
        )
        db.add(question)

    db.commit()
    print(f"✅ Loaded {len(data.get('questions', []))} sample questions")


def create_test_user(db: Session):
    """
    Create a test user for trying the application.

    Args:
        db: Database session.
    """
    # Check if test user already exists
    existing = db.query(User).filter(User.username == "student").first()
    if existing:
        print("ℹ️  Test user 'student' already exists")
        return existing

    # Create test user (password hashing will be implemented with auth system)
    user = User(
        username="student",
        email="student@codecraze.test",
        hashed_password="password123",  # Placeholder - will be hashed when auth is implemented
        full_name="Test Student",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create default preferences
    preferences = UserPreference(
        user_id=user.id,
        practice_mode="balanced",
        show_explanations=True,
        show_hints=True
    )
    db.add(preferences)
    db.commit()

    print(f"✅ Created test user: username='student', password='password123'")
    return user


def create_sample_badges(db: Session):
    """
    Create sample achievement badges.

    Args:
        db: Database session.
    """
    # Clear existing badges
    db.query(Badge).delete()

    badges = [
        {
            "badge_id": "python_master",
            "name": "Python Master",
            "description": "Achieve 95%+ accuracy on Python questions",
            "icon": "🐍",
            "category": "topic_mastery",
            "criteria": {"topic": "4", "accuracy": 0.95, "min_attempts": 10}
        },
        {
            "badge_id": "karel_commander",
            "name": "Karel Commander",
            "description": "Master all Karel programming concepts",
            "icon": "🤖",
            "category": "topic_mastery",
            "criteria": {"topic": "1", "accuracy": 0.90, "min_attempts": 15}
        },
        {
            "badge_id": "first_perfect",
            "name": "First Perfect",
            "description": "Score 100% on any quiz",
            "icon": "🎯",
            "category": "achievement",
            "criteria": {"perfect_score": True}
        },
        {
            "badge_id": "ai_expert",
            "name": "AI Expert",
            "description": "Master all AI & Machine Learning concepts",
            "icon": "🧠",
            "category": "topic_mastery",
            "criteria": {"topic": "2", "accuracy": 0.90, "min_attempts": 15}
        },
        {
            "badge_id": "crypto_specialist",
            "name": "Crypto Specialist",
            "description": "Master all cryptography concepts",
            "icon": "🔐",
            "category": "topic_mastery",
            "criteria": {"topic": "3", "accuracy": 0.90, "min_attempts": 15}
        },
        {
            "badge_id": "quantum_pioneer",
            "name": "Quantum Pioneer",
            "description": "Master quantum computing basics",
            "icon": "⚛️",
            "category": "topic_mastery",
            "criteria": {"topic": "5", "accuracy": 0.85, "min_attempts": 10}
        },
        {
            "badge_id": "competition_ready",
            "name": "Competition Ready",
            "description": "Achieve 80%+ overall readiness score",
            "icon": "🏆",
            "category": "achievement",
            "criteria": {"readiness_score": 80}
        },
        {
            "badge_id": "streak_master",
            "name": "Streak Master",
            "description": "Answer 10 questions correctly in a row",
            "icon": "🔥",
            "category": "achievement",
            "criteria": {"streak": 10}
        }
    ]

    for badge_data in badges:
        badge = Badge(**badge_data)
        db.add(badge)

    db.commit()
    print(f"✅ Created {len(badges)} sample badges")


def seed_database():
    """
    Main function to seed the database with sample data.
    """
    print("\n🌱 Seeding database with sample data...\n")

    # Initialize database
    init_db()
    print("✅ Database initialized\n")

    # Create session
    db = SessionLocal()

    try:
        # Load sample questions
        load_sample_questions(db)

        # Create test user
        create_test_user(db)

        # Create sample badges
        create_sample_badges(db)

        print("\n✅ Database seeding complete!")
        print("\n📝 You can now log in with:")
        print("   Username: student")
        print("   Password: password123")
        print("\n🚀 Start the server with: uv run backend/server.py")

    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
