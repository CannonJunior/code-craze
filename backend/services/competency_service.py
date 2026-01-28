"""
Competency tracking service.

Tracks user performance across topics and calculates mastery levels.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import yaml
from pathlib import Path

from backend.database.models import UserCompetency, QuestionAttempt, User


# Load topic taxonomy
TOPICS_FILE = Path(__file__).parent.parent.parent / "content" / "config" / "topics.yaml"
try:
    with open(TOPICS_FILE, "r") as f:
        TOPICS_CONFIG = yaml.safe_load(f)
except FileNotFoundError:
    TOPICS_CONFIG = {"topics": [], "mastery_levels": {}}


def get_or_create_competency(
    db: Session,
    user_id: int,
    topic_id: str
) -> UserCompetency:
    """
    Get existing competency or create new one.

    Args:
        db: Database session.
        user_id: User ID.
        topic_id: Topic identifier.

    Returns:
        UserCompetency: Competency record.
    """
    competency = db.query(UserCompetency).filter(
        UserCompetency.user_id == user_id,
        UserCompetency.topic_id == topic_id
    ).first()

    if not competency:
        competency = UserCompetency(
            user_id=user_id,
            topic_id=topic_id,
            mastery_level="novice"
        )
        db.add(competency)
        db.commit()
        db.refresh(competency)

    return competency


def update_competency(
    db: Session,
    user_id: int,
    topic_id: str,
    is_correct: bool,
    time_spent_ms: int
) -> UserCompetency:
    """
    Update competency after a question attempt.

    Calculates new accuracy and mastery level.

    Args:
        db: Database session.
        user_id: User ID.
        topic_id: Topic identifier.
        is_correct: Whether answer was correct.
        time_spent_ms: Time spent on question in milliseconds.

    Returns:
        UserCompetency: Updated competency record.
    """
    competency = get_or_create_competency(db, user_id, topic_id)

    # Update statistics
    competency.total_attempts += 1
    if is_correct:
        competency.correct_attempts += 1
    competency.total_time_ms += time_spent_ms
    competency.last_practiced = datetime.utcnow()

    # Calculate new mastery level
    accuracy = competency.accuracy
    attempts = competency.total_attempts

    mastery_levels = TOPICS_CONFIG.get("mastery_levels", {})

    # Determine mastery level based on accuracy and attempts
    new_mastery = "novice"
    for level_name in ["master", "expert", "proficient", "developing", "novice"]:
        level_criteria = mastery_levels.get(level_name, {})
        min_accuracy = level_criteria.get("min_accuracy", 0.0)
        min_attempts = level_criteria.get("min_attempts", 0)

        if accuracy >= min_accuracy and attempts >= min_attempts:
            new_mastery = level_name
            break

    competency.mastery_level = new_mastery
    competency.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(competency)

    return competency


def get_user_competencies(
    db: Session,
    user_id: int
) -> List[Dict]:
    """
    Get all competencies for a user.

    Args:
        db: Database session.
        user_id: User ID.

    Returns:
        list: List of competency dictionaries with topic info.
    """
    competencies = db.query(UserCompetency).filter(
        UserCompetency.user_id == user_id
    ).all()

    result = []
    for comp in competencies:
        topic_info = get_topic_info(comp.topic_id)
        trend = calculate_trend(db, user_id, comp.topic_id)

        result.append({
            "topic_id": comp.topic_id,
            "topic_name": topic_info.get("name", comp.topic_id),
            "mastery_level": comp.mastery_level,
            "accuracy": comp.accuracy,
            "total_attempts": comp.total_attempts,
            "avg_time_ms": comp.avg_time_ms,
            "last_practiced": comp.last_practiced,
            "trend": trend,
        })

    return result


def get_topic_info(topic_id: str) -> Dict:
    """
    Get topic information from taxonomy.

    Args:
        topic_id: Topic identifier (e.g., "2.1").

    Returns:
        dict: Topic information including name and description.
    """
    # Parse topic ID (e.g., "2.1" -> main=2, sub=1)
    parts = topic_id.split(".")
    if len(parts) == 1:
        main_id = parts[0]
        sub_id = None
    else:
        main_id = parts[0]
        sub_id = ".".join(parts)

    # Search for topic in config
    for topic in TOPICS_CONFIG.get("topics", []):
        if topic["id"] == main_id:
            if sub_id:
                # Look for subtopic
                for subtopic in topic.get("subtopics", []):
                    if subtopic["id"] == sub_id:
                        return subtopic
                return {"name": sub_id, "description": ""}
            else:
                return topic

    return {"name": topic_id, "description": ""}


def calculate_trend(
    db: Session,
    user_id: int,
    topic_id: str,
    lookback_attempts: int = 10
) -> str:
    """
    Calculate performance trend for a topic.

    Compares recent performance to earlier performance.

    Args:
        db: Database session.
        user_id: User ID.
        topic_id: Topic identifier.
        lookback_attempts: Number of recent attempts to consider.

    Returns:
        str: "improving", "stable", or "declining".
    """
    # Get recent attempts for this topic
    attempts = db.query(QuestionAttempt).filter(
        QuestionAttempt.user_id == user_id,
        QuestionAttempt.topic_id == topic_id
    ).order_by(QuestionAttempt.created_at.desc()).limit(lookback_attempts * 2).all()

    if len(attempts) < lookback_attempts:
        return "stable"

    # Split into recent and earlier
    recent = attempts[:lookback_attempts]
    earlier = attempts[lookback_attempts:lookback_attempts * 2]

    # Calculate accuracy for each
    recent_accuracy = sum(1 for a in recent if a.is_correct) / len(recent)
    earlier_accuracy = sum(1 for a in earlier if a.is_correct) / len(earlier)

    # Determine trend
    diff = recent_accuracy - earlier_accuracy
    if diff > 0.1:
        return "improving"
    elif diff < -0.1:
        return "declining"
    else:
        return "stable"


def get_weak_areas(
    db: Session,
    user_id: int,
    min_attempts: int = 5,
    accuracy_threshold: float = 0.70
) -> List[Dict]:
    """
    Identify weak areas that need more practice.

    Args:
        db: Database session.
        user_id: User ID.
        min_attempts: Minimum attempts before considering a topic.
        accuracy_threshold: Topics below this accuracy are considered weak.

    Returns:
        list: List of weak topics with recommendations.
    """
    competencies = db.query(UserCompetency).filter(
        UserCompetency.user_id == user_id,
        UserCompetency.total_attempts >= min_attempts
    ).all()

    weak_areas = []
    for comp in competencies:
        if comp.accuracy < accuracy_threshold:
            topic_info = get_topic_info(comp.topic_id)
            weak_areas.append({
                "topic_id": comp.topic_id,
                "topic_name": topic_info.get("name", comp.topic_id),
                "accuracy": comp.accuracy,
                "total_attempts": comp.total_attempts,
                "mastery_level": comp.mastery_level,
                "reason": f"Current accuracy ({comp.accuracy:.1%}) is below target ({accuracy_threshold:.1%})",
            })

    # Sort by accuracy (weakest first)
    weak_areas.sort(key=lambda x: x["accuracy"])

    return weak_areas


def calculate_competition_readiness(
    db: Session,
    user_id: int
) -> Tuple[int, Dict]:
    """
    Calculate overall competition readiness score (0-100).

    Args:
        db: Database session.
        user_id: User ID.

    Returns:
        tuple: (readiness_score, breakdown_dict)
    """
    competencies = get_user_competencies(db, user_id)

    if not competencies:
        return 0, {
            "coverage": 0,
            "accuracy": 0,
            "mastery": 0,
            "total": 0,
        }

    # Calculate metrics
    total_topics = len(TOPICS_CONFIG.get("topics", []))
    topics_started = len(competencies)
    coverage_score = (topics_started / total_topics) * 100 if total_topics > 0 else 0

    avg_accuracy = sum(c["accuracy"] for c in competencies) / len(competencies)
    accuracy_score = avg_accuracy * 100

    mastery_weights = {"novice": 0, "developing": 0.5, "proficient": 0.75, "expert": 0.9, "master": 1.0}
    avg_mastery = sum(mastery_weights.get(c["mastery_level"], 0) for c in competencies) / len(competencies)
    mastery_score = avg_mastery * 100

    # Overall score (weighted average)
    overall_score = int(
        coverage_score * 0.3 +
        accuracy_score * 0.4 +
        mastery_score * 0.3
    )

    breakdown = {
        "coverage": int(coverage_score),
        "accuracy": int(accuracy_score),
        "mastery": int(mastery_score),
        "total": overall_score,
    }

    return overall_score, breakdown


def get_recommendations(
    db: Session,
    user_id: int,
    max_recommendations: int = 3
) -> List[str]:
    """
    Get personalized learning recommendations.

    Args:
        db: Database session.
        user_id: User ID.
        max_recommendations: Maximum number of recommendations.

    Returns:
        list: List of recommendation strings.
    """
    recommendations = []

    # Check for weak areas
    weak_areas = get_weak_areas(db, user_id)
    if weak_areas:
        for weak in weak_areas[:max_recommendations]:
            recommendations.append(
                f"Focus on {weak['topic_name']} (current accuracy: {weak['accuracy']:.1%})"
            )

    # Check for topics not practiced recently
    competencies = db.query(UserCompetency).filter(
        UserCompetency.user_id == user_id,
        UserCompetency.last_practiced < datetime.utcnow() - timedelta(days=3)
    ).order_by(UserCompetency.last_practiced).limit(max_recommendations).all()

    for comp in competencies:
        if len(recommendations) < max_recommendations:
            topic_info = get_topic_info(comp.topic_id)
            days_ago = (datetime.utcnow() - comp.last_practiced).days
            recommendations.append(
                f"Review {topic_info.get('name', comp.topic_id)} (last practiced {days_ago} days ago)"
            )

    # If no specific recommendations, suggest next level
    if not recommendations:
        recommendations.append("Continue practicing to maintain your skills!")

    return recommendations[:max_recommendations]
