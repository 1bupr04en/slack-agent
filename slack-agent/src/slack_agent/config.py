"""Configuration management using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from typing import Literal


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SLOTH_", env_file=".env", extra="ignore")
    
    camera_index: int = Field(0, description="Camera device index", ge=0)
    absent_frame_threshold: int = Field(30, description="Frames without face to consider 'absent'", gt=0)
    leave_seconds: float = Field(60.0, description="Seconds of absence before sloth mode", gt=0)
    detection_fps: float = Field(20.0, description="Frames per second for detection", gt=0)
    face_detector_backend: str = Field("haar", description="'haar' or 'mediapipe'")
    agent_window_title: str = Field("YourAgentName", description="Agent window title for resume/pause")
    health_check_interval: float = Field(30.0, description="Seconds between health checks", gt=0)
    camera_reopen_retries: int = Field(3, description="Retries for camera open failure", gt=0)
    log_level: str = Field("INFO", description="Logging level")
    
    @property
    def detection_interval(self) -> float:
        return 1.0 / self.detection_fps


settings = Settings()
