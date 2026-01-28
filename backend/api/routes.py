"""
API routes for Code Craze Study Guide.

This module defines all API endpoints for the application.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.database.db import get_db
from backend.api import models as api_models
from backend.database import models as db_models
from backend.services import competency_service, adaptive_learning

# Create main router
router = APIRouter()


# ============================================================================
# Health and Info Endpoints
# ============================================================================

@router.get("/info")
async def get_info():
    """
    Get application information.

    Returns:
        dict: Application name, version, and description.
    """
    return {
        "name": "Code Craze Academy",
        "version": "0.1.0",
        "description": "Interactive learning platform for Science Olympiad Code Craze",
        "port": 8989,
    }


# ============================================================================
# User Endpoints (placeholder - will be implemented with auth)
# ============================================================================

@router.get("/users/me")
async def get_current_user():
    """
    Get current authenticated user.

    TODO: Implement authentication.

    Returns:
        dict: User information.
    """
    return {"message": "Authentication not yet implemented"}


# ============================================================================
# Competency Endpoints
# ============================================================================

@router.get("/competencies")
async def get_competencies(db: Session = Depends(get_db)):
    """
    Get user's competency dashboard.

    Shows accuracy, mastery level, and trends across all topics.

    Args:
        db: Database session.

    Returns:
        dict: Competency dashboard data.
    """
    # TODO: Get user_id from authentication
    # For now, use test user (id=1)
    user_id = 1

    # Get competencies
    competencies = competency_service.get_user_competencies(db, user_id)

    # Calculate competition readiness
    readiness, breakdown = competency_service.calculate_competition_readiness(db, user_id)

    # Get recommendations
    recommendations = competency_service.get_recommendations(db, user_id)

    return {
        "overall_progress": breakdown.get("total", 0),
        "competition_readiness": readiness,
        "competencies": competencies,
        "recommendations": recommendations,
    }


@router.get("/competencies/{topic_id}")
async def get_topic_competency(topic_id: str, db: Session = Depends(get_db)):
    """
    Get detailed competency for a specific topic.

    Args:
        topic_id: Topic identifier (e.g., "1.1_karel_commands").
        db: Database session.

    Returns:
        dict: Detailed topic competency data.
    """
    # TODO: Implement after authentication
    return {
        "topic_id": topic_id,
        "mastery_level": "novice",
        "accuracy": 0.0,
        "total_attempts": 0,
    }


@router.get("/recommendations")
async def get_recommendations(db: Session = Depends(get_db)):
    """
    Get recommended focus areas based on competencies.

    Analyzes user performance and suggests topics to practice.

    Args:
        db: Database session.

    Returns:
        list: Recommended topics with reasons.
    """
    # TODO: Implement recommendation algorithm
    return {
        "recommendations": [],
    }


# ============================================================================
# Practice Session Endpoints
# ============================================================================

@router.post("/practice/start")
async def start_practice_session(
    request: api_models.PracticeStartRequest,
    db: Session = Depends(get_db)
):
    """
    Start a new practice session.

    Selects questions based on user's practice mode and competencies.

    Args:
        request: Practice session configuration.
        db: Database session.

    Returns:
        dict: Practice session ID and first question.
    """
    # TODO: Get user_id from authentication
    user_id = 1

    # Select first question using adaptive algorithm
    question, context = adaptive_learning.select_next_question(
        db,
        user_id,
        practice_mode=request.mode.value,
        topic_filter=request.topic_filter,
        difficulty=request.difficulty
    )

    # Format question for response
    question_data = None
    if question:
        # Remove 'correct' flag from answers for the user
        answers_for_user = [
            {"text": ans["text"]} for ans in question.answers
        ]

        question_data = {
            "id": question.id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "topic_id": question.topic_id,
            "difficulty": question.difficulty,
            "answers": answers_for_user,
            "code_snippet": question.code_snippet,
            "image_url": question.image_url,
            "practice_context": context
        }

    return {
        "session_id": f"session_{user_id}",
        "mode": request.mode,
        "question": question_data,
    }


@router.get("/practice/next")
async def get_next_question(
    session_id: str,
    mode: str = "balanced",
    db: Session = Depends(get_db)
):
    """
    Get next question in practice session.

    Uses adaptive algorithm to select question based on user competencies.

    Args:
        session_id: Practice session identifier.
        mode: Practice mode (balanced, weak_focus, review, competition).
        db: Database session.

    Returns:
        dict: Next question.
    """
    # TODO: Get user_id from authentication
    user_id = 1

    # Select next question using adaptive algorithm
    question, context = adaptive_learning.select_next_question(
        db,
        user_id,
        practice_mode=mode
    )

    # Format question for response
    question_data = None
    if question:
        # Remove 'correct' flag from answers for the user
        answers_for_user = [
            {"text": ans["text"]} for ans in question.answers
        ]

        question_data = {
            "id": question.id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "topic_id": question.topic_id,
            "difficulty": question.difficulty,
            "answers": answers_for_user,
            "code_snippet": question.code_snippet,
            "image_url": question.image_url,
            "practice_context": context
        }

    return {
        "question": question_data,
        "context": context,
    }


@router.post("/practice/submit")
async def submit_answer(
    request: api_models.AnswerSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submit answer and get detailed explanation.

    Records attempt, updates competencies, and returns explanation.

    Args:
        request: Answer submission data.
        db: Database session.

    Returns:
        dict: Result, explanation, and competency update.
    """
    # TODO: Get user_id from authentication
    user_id = 1

    # Get the question
    question = db.query(db_models.Question).filter(
        db_models.Question.id == request.question_id
    ).first()

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Check if answer is correct
    correct_answer_index = next(
        (i for i, ans in enumerate(question.answers) if ans.get("correct")),
        None
    )

    is_correct = (request.selected_answer == correct_answer_index)

    # Record the attempt
    attempt = db_models.QuestionAttempt(
        user_id=user_id,
        question_id=question.id,
        topic_id=question.topic_id,
        selected_answer=request.selected_answer,
        is_correct=is_correct,
        time_spent_ms=request.time_spent_ms,
        hints_used=request.hints_used
    )
    db.add(attempt)

    # Update competency
    updated_competency = competency_service.update_competency(
        db,
        user_id,
        question.topic_id,
        is_correct,
        request.time_spent_ms
    )

    # Build explanation
    user_answer = question.answers[request.selected_answer]
    correct_answer = question.answers[correct_answer_index]

    explanation = {
        "your_answer": {
            "text": user_answer["text"],
            "why_wrong": user_answer.get("explanation") if not is_correct else None,
            "common_mistake": user_answer.get("common_mistake") if not is_correct else None
        },
        "correct_answer": {
            "text": correct_answer["text"],
            "why_right": correct_answer.get("explanation"),
            "teaching_point": correct_answer.get("teaching_point")
        },
        "solution_steps": question.solution_steps,
        "lesson_link": f"/lessons/{question.lesson_reference}" if question.lesson_reference else None
    }

    competency_update = {
        "topic": question.topic_id,
        "new_accuracy": updated_competency.accuracy,
        "mastery_level": updated_competency.mastery_level,
        "total_attempts": updated_competency.total_attempts
    }

    db.commit()

    return {
        "result": "correct" if is_correct else "incorrect",
        "selected_answer": request.selected_answer,
        "correct_answer": correct_answer_index,
        "explanation": explanation,
        "competency_update": competency_update,
    }


# ============================================================================
# User Preferences Endpoints
# ============================================================================

@router.get("/preferences")
async def get_preferences(db: Session = Depends(get_db)):
    """
    Get user preferences.

    Args:
        db: Database session.

    Returns:
        dict: User preferences.
    """
    # TODO: Implement after authentication
    return {
        "practice_mode": "balanced",
        "show_explanations": True,
        "show_hints": True,
    }


@router.put("/preferences")
async def update_preferences(
    request: api_models.PreferencesUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update user preferences.

    Args:
        request: Updated preferences.
        db: Database session.

    Returns:
        dict: Updated preferences.
    """
    # TODO: Implement preference updates
    return request.model_dump()


# ============================================================================
# Progress Endpoints
# ============================================================================

@router.get("/progress")
async def get_progress(db: Session = Depends(get_db)):
    """
    Get user's learning progress.

    Shows completion status and scores for all levels.

    Args:
        db: Database session.

    Returns:
        dict: Progress data.
    """
    # TODO: Implement after authentication
    return {
        "levels": [],
        "total_points": 0,
        "badges_earned": 0,
    }
