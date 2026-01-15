from enum import Enum

class ProcessingStatus(Enum):
    """Status of image processing job"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting_for_inputs"