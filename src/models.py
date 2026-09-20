from pydantic import BaseModel, Field, validator, model_validator
from typing import Optional
from datetime import datetime

class ScriptLine(BaseModel):
    """Represents a single line of dialogue in the script."""
    speaker: str  # "Sarah" or "Alex"
    content: str
    line_number: int

class Script(BaseModel):
    """Represents a complete video script."""
    topic: str
    lines: list[ScriptLine]
    word_count: int
    estimated_duration_minutes: float
    generated_at: datetime = Field(default_factory=datetime.now)
    target_words: Optional[int] = Field(None, description="Target word count for the script")

    @model_validator(mode='after')
    def validate_word_count(self):
        from .config import SCRIPT_MIN_WORDS, SCRIPT_MAX_WORDS

        # For custom target words: allow ±35% tolerance for flexibility
        # (Claude varies significantly, especially for longer scripts)
        if self.target_words:
            target = self.target_words
            # Allow generous tolerance: target ±35%
            tolerance = int(target * 0.35)
            min_words = max(800, target - tolerance)  # Minimum 800 words
            max_words = target + tolerance
        else:
            # Default range for standard generation
            min_words = SCRIPT_MIN_WORDS
            max_words = SCRIPT_MAX_WORDS

        if not (min_words <= self.word_count <= max_words):
            raise ValueError(f"Word count must be between {min_words} and {max_words}, got {self.word_count}")
        return self

class SEOMetadata(BaseModel):
    """YouTube SEO metadata for a video."""
    title: str
    description: str
    hashtags: list[str]
    tags: list[str]

    @validator("title")
    def validate_title_length(cls, v):
        if len(v) > 65:
            raise ValueError(f"Title must be 65 characters or less, got {len(v)}")
        return v

    @validator("hashtags")
    def validate_hashtags_count(cls, v):
        if not (15 <= len(v) <= 20):
            raise ValueError(f"Must have 15-20 hashtags, got {len(v)}")
        return v

    @validator("tags")
    def validate_tags_count(cls, v):
        if not (15 <= len(v) <= 20):
            raise ValueError(f"Must have 15-20 tags, got {len(v)}")
        return v

class TopicInput(BaseModel):
    """User input for video generation."""
    topic: str = Field(..., description="The topic for the video")
    optional_context: Optional[str] = Field(None, description="Additional context or requirements")
    target_words: Optional[int] = Field(None, description="Target word count for the script")

    @validator("topic")
    def validate_topic(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Topic must be at least 3 characters")
        return v.strip()

class VideoOutput(BaseModel):
    """Complete video generation output metadata."""
    topic: str
    topic_slug: str  # URL-friendly version
    script: Script
    seo_metadata: Optional[SEOMetadata] = None
    output_folder: str
    created_at: datetime = Field(default_factory=datetime.now)
    files: dict = Field(default_factory=dict)  # Maps filename to path
