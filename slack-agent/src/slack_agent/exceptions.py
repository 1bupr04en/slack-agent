"""Custom exceptions for the slouch mode plugin."""


class CameraError(Exception):
    """Raised when camera cannot be opened or read."""
    pass


class WorkflowError(Exception):
    """Raised when pausing/resuming the Agent fails."""
    pass
