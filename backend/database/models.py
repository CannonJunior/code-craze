"""
SQLAlchemy database models for Code Craze application.

This module defines all database tables including users, competency tracking,
questions, and gamification elements.
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database.db import Base


class User(Base):
    """User account model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    competencies = relationship("UserCompetency", back_populates="user", cascade="all, delete-orphan")
    question_attempts = relationship("QuestionAttempt", back_populates="user", cascade="all, delete-orphan")
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="user", cascade="all, delete-orphan")


class UserCompetency(Base):
    """
    Track user competency across different coding topics.

    Stores accuracy, attempts, and mastery level for each topic.
    """

    __tablename__ = "user_competencies"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(String(50), nullable=False, index=True)  # e.g., "1.1_karel_commands"
    total_attempts = Column(Integer, default=0)
    correct_attempts = Column(Integer, default=0)
    total_time_ms = Column(Integer, default=0)  # Total time spent on this topic
    last_practiced = Column(DateTime(timezone=True))
    mastery_level = Column(String(20), default="novice")  # novice, developing, proficient, expert, master
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="competencies")

    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        if self.total_attempts == 0:
            return 0.0
        return self.correct_attempts / self.total_attempts

    @property
    def avg_time_ms(self) -> float:
        """Calculate average time per attempt in milliseconds."""
        if self.total_attempts == 0:
            return 0.0
        return self.total_time_ms / self.total_attempts


class QuestionAttempt(Base):
    """
    Record of each question attempt by a user.

    Stores detailed information for analytics and adaptive learning.
    """

    __tablename__ = "question_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    topic_id = Column(String(50), nullable=False, index=True)
    selected_answer = Column(Integer)  # Index of selected answer
    is_correct = Column(Boolean, nullable=False)
    time_spent_ms = Column(Integer)  # Time to answer in milliseconds
    hints_used = Column(Integer, default=0)
    attempt_number = Column(Integer, default=1)  # For same question retries
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="question_attempts")
    question = relationship("Question", back_populates="attempts")


class UserPreference(Base):
    """
    User preferences for adaptive learning and UI settings.
    """

    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    practice_mode = Column(String(20), default="balanced")  # balanced, weak_focus, review, competition
    show_explanations = Column(Boolean, default=True)
    show_hints = Column(Boolean, default=True)
    difficulty_level = Column(String(20), default="adaptive")  # adaptive, easy, medium, hard
    theme = Column(String(20), default="light")  # light, dark
    sound_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="preferences")


class Question(Base):
    """
    Question bank with detailed explanations.

    Stores questions with multiple answers, explanations, and solution steps.
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(20), nullable=False)  # multiple_choice, code_trace, code_completion, matching
    topic_id = Column(String(50), nullable=False, index=True)
    difficulty = Column(Integer, default=1)  # 1-5 scale

    # JSON fields for structured data
    # answers: [{"text": "...", "correct": bool, "explanation": "...", "common_mistake": "..."}]
    answers = Column(JSON, nullable=False)

    # solution_steps: ["Step 1: ...", "Step 2: ...", ...]
    solution_steps = Column(JSON)

    # Optional code snippet for code-related questions
    code_snippet = Column(Text)

    lesson_reference = Column(String(50))  # Link to lesson
    image_url = Column(String(200))  # Optional diagram/image
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    attempts = relationship("QuestionAttempt", back_populates="question")


class Badge(Base):
    """
    Badge definitions for gamification.
    """

    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    badge_id = Column(String(50), unique=True, nullable=False)  # e.g., "python_master"
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(50))  # Emoji or icon identifier
    category = Column(String(30))  # topic_mastery, achievement, collection
    criteria = Column(JSON)  # Criteria for earning (e.g., {"accuracy": 0.95, "topic": "4"})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user_badges = relationship("UserBadge", back_populates="badge")


class UserBadge(Base):
    """
    Badges earned by users.
    """

    __tablename__ = "user_badges"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="user_badges")


class Progress(Base):
    """
    User progress through learning levels.
    """

    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    level = Column(Integer, nullable=False)  # 0-10
    status = Column(String(20), default="locked")  # locked, in_progress, completed
    score = Column(Float)  # Quiz score (0-100)
    time_spent_ms = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="progress")
