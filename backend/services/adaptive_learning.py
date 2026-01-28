"""
Adaptive learning service for question selection.

Implements algorithms to select optimal questions based on user competency
and practice mode.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Dict, Tuple
import random

from backend.database.models import Question, UserCompetency, QuestionAttempt
from backend.services.competency_service import get_user_competencies, get_weak_areas


def select_next_question(
    db: Session,
    user_id: int,
    practice_mode: str = "balanced",
    topic_filter: Optional[list] = None,
    difficulty: Optional[int] = None,
    exclude_recent: int = 10
) -> Tuple[Optional[Question], str]:
    """
    Select next question using adaptive algorithm.

    Args:
        db: Database session.
        user_id: User ID.
        practice_mode: Mode (balanced, weak_focus, review, competition).
        topic_filter: Optional list of topic IDs to filter by.
        difficulty: Optional difficulty (1-5), None = adaptive.
        exclude_recent: Exclude recently answered questions.

    Returns:
        tuple: (Question object, context string explaining selection)
    """
    # Get topic weights based on practice mode
    topic_weights = calculate_topic_weights(db, user_id, practice_mode)

    if not topic_weights:
        # No competency data yet, select random question
        question = select_random_question(db, topic_filter, difficulty)
        return question, "Starting your learning journey!"

    # Select topic based on weighted probability
    selected_topic = weighted_random_choice(topic_weights)

    # Get recently answered question IDs to avoid
    recent_question_ids = get_recent_question_ids(db, user_id, exclude_recent)

    # Select question from topic
    question = select_question_from_topic(
        db,
        selected_topic,
        difficulty,
        recent_question_ids
    )

    if not question:
        # Fallback to any available question
        question = select_random_question(db, topic_filter, difficulty, recent_question_ids)

    # Generate context string
    competencies = get_user_competencies(db, user_id)
    topic_comp = next((c for c in competencies if c["topic_id"] == selected_topic), None)

    if topic_comp and practice_mode == "weak_focus":
        context = f"Practicing: {topic_comp['topic_name']} (Your accuracy: {topic_comp['accuracy']:.0%})"
    elif topic_comp:
        context = f"Practicing: {topic_comp['topic_name']}"
    else:
        context = "Exploring new topics"

    return question, context


def calculate_topic_weights(
    db: Session,
    user_id: int,
    practice_mode: str
) -> Dict[str, float]:
    """
    Calculate topic weights based on practice mode.

    Args:
        db: Database session.
        user_id: User ID.
        practice_mode: Mode (balanced, weak_focus, review, competition).

    Returns:
        dict: Topic ID -> weight mapping.
    """
    competencies = get_user_competencies(db, user_id)

    if not competencies:
        return {}

    weights = {}

    if practice_mode == "weak_focus":
        # Weight topics inversely to accuracy (lower accuracy = higher weight)
        for comp in competencies:
            accuracy = comp["accuracy"]
            attempts = comp["total_attempts"]

            # Only focus on topics with enough attempts
            if attempts >= 5:
                if accuracy < 0.70:
                    # High weight for struggling topics
                    weight = (1.0 - accuracy) * 2.0
                elif accuracy < 0.85:
                    # Medium weight for developing topics
                    weight = (1.0 - accuracy)
                else:
                    # Low weight for mastered topics (but still possible)
                    weight = 0.1
            else:
                # Medium weight for new topics
                weight = 0.5

            weights[comp["topic_id"]] = weight

    elif practice_mode == "review":
        # Weight topics based on time since last practice
        from datetime import datetime, timedelta
        now = datetime.utcnow()

        for comp in competencies:
            if comp["last_practiced"]:
                days_since = (now - comp["last_practiced"]).days
                # More weight for topics not practiced recently
                weight = min(days_since / 7.0, 2.0)  # Cap at 2.0
            else:
                weight = 2.0  # Never practiced

            weights[comp["topic_id"]] = weight

    elif practice_mode == "competition":
        # Uniform distribution (realistic competition simulation)
        for comp in competencies:
            weights[comp["topic_id"]] = 1.0

    else:  # balanced mode
        # Mix of current level (50%), review (30%), weak areas (20%)
        weak_areas = get_weak_areas(db, user_id)
        weak_topic_ids = {area["topic_id"] for area in weak_areas}

        for comp in competencies:
            topic_id = comp["topic_id"]
            attempts = comp["total_attempts"]

            if topic_id in weak_topic_ids:
                # Weak areas get higher weight
                weight = 1.5
            elif attempts > 0 and comp["accuracy"] > 0.85:
                # Mastered topics get lower weight (review)
                weight = 0.5
            else:
                # Current learning topics get normal weight
                weight = 1.0

            weights[topic_id] = weight

    return weights


def weighted_random_choice(weights: Dict[str, float]) -> str:
    """
    Select a random item based on weights.

    Args:
        weights: Dictionary of item -> weight.

    Returns:
        str: Selected item.
    """
    if not weights:
        raise ValueError("Weights dictionary is empty")

    items = list(weights.keys())
    weight_values = list(weights.values())

    # Handle all zero weights
    if all(w == 0 for w in weight_values):
        return random.choice(items)

    return random.choices(items, weights=weight_values, k=1)[0]


def get_recent_question_ids(
    db: Session,
    user_id: int,
    count: int
) -> set:
    """
    Get recently answered question IDs.

    Args:
        db: Database session.
        user_id: User ID.
        count: Number of recent questions.

    Returns:
        set: Set of recent question IDs.
    """
    recent = db.query(QuestionAttempt.question_id).filter(
        QuestionAttempt.user_id == user_id
    ).order_by(QuestionAttempt.created_at.desc()).limit(count).all()

    return {q[0] for q in recent}


def select_question_from_topic(
    db: Session,
    topic_id: str,
    difficulty: Optional[int],
    exclude_ids: set
) -> Optional[Question]:
    """
    Select a question from a specific topic.

    Args:
        db: Database session.
        topic_id: Topic identifier.
        difficulty: Optional difficulty level.
        exclude_ids: Set of question IDs to exclude.

    Returns:
        Question: Selected question or None.
    """
    query = db.query(Question).filter(Question.topic_id == topic_id)

    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    if exclude_ids:
        query = query.filter(~Question.id.in_(exclude_ids))

    # Get all matching questions
    questions = query.all()

    if not questions:
        return None

    # Select random question from matches
    return random.choice(questions)


def select_random_question(
    db: Session,
    topic_filter: Optional[list],
    difficulty: Optional[int],
    exclude_ids: Optional[set] = None
) -> Optional[Question]:
    """
    Select a random question (fallback method).

    Args:
        db: Database session.
        topic_filter: Optional topic filter.
        difficulty: Optional difficulty filter.
        exclude_ids: Optional set of IDs to exclude.

    Returns:
        Question: Random question or None.
    """
    query = db.query(Question)

    if topic_filter:
        query = query.filter(Question.topic_id.in_(topic_filter))

    if difficulty:
        query = query.filter(Question.difficulty == difficulty)

    if exclude_ids:
        query = query.filter(~Question.id.in_(exclude_ids))

    # Random selection using SQL
    question = query.order_by(func.random()).first()

    return question


def adapt_difficulty(
    db: Session,
    user_id: int,
    topic_id: str
) -> int:
    """
    Suggest difficulty level based on user performance.

    Args:
        db: Database session.
        user_id: User ID.
        topic_id: Topic identifier.

    Returns:
        int: Suggested difficulty (1-5).
    """
    comp = db.query(UserCompetency).filter(
        UserCompetency.user_id == user_id,
        UserCompetency.topic_id == topic_id
    ).first()

    if not comp or comp.total_attempts < 5:
        # Start with easy questions
        return 2

    accuracy = comp.accuracy

    # Adjust difficulty based on accuracy
    if accuracy >= 0.90:
        return 5  # Hard
    elif accuracy >= 0.80:
        return 4  # Medium-hard
    elif accuracy >= 0.70:
        return 3  # Medium
    elif accuracy >= 0.60:
        return 2  # Easy-medium
    else:
        return 1  # Easy


def should_show_hint(
    db: Session,
    user_id: int,
    topic_id: str,
    time_spent_ms: int
) -> bool:
    """
    Determine if a hint should be offered.

    Based on user performance and time spent.

    Args:
        db: Database session.
        user_id: User ID.
        topic_id: Topic identifier.
        time_spent_ms: Time already spent on question.

    Returns:
        bool: True if hint should be offered.
    """
    comp = db.query(UserCompetency).filter(
        UserCompetency.user_id == user_id,
        UserCompetency.topic_id == topic_id
    ).first()

    # Offer hint if struggling (low accuracy and taking long time)
    if comp and comp.accuracy < 0.60 and time_spent_ms > 60000:  # 1 minute
        return True

    # Offer hint if taking very long time regardless
    if time_spent_ms > 180000:  # 3 minutes
        return True

    return False
