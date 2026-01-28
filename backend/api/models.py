"""
Pydantic models for API request/response validation.

These models define the structure of data sent to and from the API.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# Enums
# ============================================================================

class PracticeMode(str, Enum):
    """Practice session modes."""
    BALANCED = "balanced"
    WEAK_FOCUS = "weak_focus"
    REVIEW = "review"
    COMPETITION = "competition"


class QuestionType(str, Enum):
    """Question types."""
    MULTIPLE_CHOICE = "multiple_choice"
    CODE_TRACE = "code_trace"
    CODE_COMPLETION = "code_completion"
    MATCHING = "matching"
    TRUE_FALSE = "true_false"


class MasteryLevel(str, Enum):
    """Mastery levels for topics."""
    NOVICE = "novice"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    EXPERT = "expert"
    MASTER = "master"


# ============================================================================
# User Models
# ============================================================================

class UserCreate(BaseModel):
    """Request model for user registration."""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """Request model for user login."""
    username: str
    password: str


class UserResponse(BaseModel):
    """Response model for user data."""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Response model for authentication tokens."""
    access_token: str
    token_type: str = "bearer"


# ============================================================================
# Practice Session Models
# ============================================================================

class PracticeStartRequest(BaseModel):
    """Request to start a practice session."""
    mode: PracticeMode = PracticeMode.BALANCED
    topic_filter: Optional[List[str]] = None  # Filter by specific topics
    difficulty: Optional[int] = None  # 1-5, None = adaptive


class AnswerSubmitRequest(BaseModel):
    """Request to submit an answer."""
    question_id: int
    selected_answer: int  # Index of selected answer
    time_spent_ms: int
    hints_used: int = 0


class AnswerExplanation(BaseModel):
    """Explanation for an answer."""
    text: str
    why_right: Optional[str] = None
    why_wrong: Optional[str] = None
    common_mistake: Optional[str] = None


class QuestionResponse(BaseModel):
    """Response model for a question."""
    id: int
    question_text: str
    question_type: QuestionType
    topic_id: str
    difficulty: int
    answers: List[Dict[str, Any]]  # List of answer objects (without correct flag for user)
    code_snippet: Optional[str] = None
    image_url: Optional[str] = None
    practice_context: Optional[str] = None  # "Practicing: X (Your accuracy: Y%)"


class AnswerSubmitResponse(BaseModel):
    """Response after submitting an answer."""
    result: str  # "correct" or "incorrect"
    selected_answer: int
    correct_answer: int
    explanation: Dict[str, Any]  # Detailed explanation object
    competency_update: Dict[str, Any]  # Updated competency stats


# ============================================================================
# Competency Models
# ============================================================================

class CompetencyResponse(BaseModel):
    """Response model for a single competency."""
    topic_id: str
    topic_name: str
    mastery_level: MasteryLevel
    accuracy: float
    total_attempts: int
    trend: str  # "improving", "stable", "declining"
    last_practiced: Optional[datetime]


class CompetencyDashboard(BaseModel):
    """Response model for competency dashboard."""
    overall_progress: float  # 0-100
    competition_readiness: int  # 0-100
    competencies: List[CompetencyResponse]
    recommendations: List[str]  # Recommended focus areas


# ============================================================================
# Preferences Models
# ============================================================================

class PreferencesUpdateRequest(BaseModel):
    """Request to update user preferences."""
    practice_mode: Optional[PracticeMode] = None
    show_explanations: Optional[bool] = None
    show_hints: Optional[bool] = None
    difficulty_level: Optional[str] = None
    theme: Optional[str] = None
    sound_enabled: Optional[bool] = None


class PreferencesResponse(BaseModel):
    """Response model for user preferences."""
    practice_mode: PracticeMode
    show_explanations: bool
    show_hints: bool
    difficulty_level: str
    theme: str
    sound_enabled: bool

    class Config:
        from_attributes = True


# ============================================================================
# Progress Models
# ============================================================================

class LevelProgress(BaseModel):
    """Progress for a single level."""
    level: int
    status: str  # locked, in_progress, completed
    score: Optional[float] = None
    time_spent_ms: int
    completed_at: Optional[datetime] = None


class ProgressResponse(BaseModel):
    """Response model for user progress."""
    levels: List[LevelProgress]
    total_points: int
    badges_earned: int
    current_level: int


# ============================================================================
# Badge Models
# ============================================================================

class BadgeResponse(BaseModel):
    """Response model for a badge."""
    id: int
    badge_id: str
    name: str
    description: str
    icon: str
    category: str
    earned: bool
    earned_at: Optional[datetime] = None

    class Config:
        from_attributes = True
