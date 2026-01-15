from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import time
from .processing_status import ProcessingStatus

@dataclass
class ImageJob:
    """Data object flowing through the pipeline - represents a photo processing job"""
    # Core identification
    image_id: str
    transformations: List[str] = field(default_factory=list)
    current_format: str = ""

    # For specific filter types
    panorama_group: Optional[str] = None          # For n-to-1 (panorama)
    split_into: Optional[int] = None              # For 1-to-n (splitting)
    quality_score: Optional[float] = None         # For 1-of-n selection
    correlation_id: Optional[str] = None          # For grouping related jobs

    # For summator/numeric operations (professor's example)
    numeric_value: Optional[float] = None

    # For cycles and iteration tracking
    cycle_count: int = 0
    iteration_limit: Optional[int] = None

    # Control signals
    is_termination: bool = False
    is_poison_pill: bool = False
    config_updates: Optional[Dict[str, Any]] = None

    # Internal tracking
    created_at: float = field(default_factory=time.time)
    status: ProcessingStatus = ProcessingStatus.PENDING
    processed_by: List[str] = field(default_factory=list)

    def add_transformation(self, transformation: str) -> 'ImageJob':
        """Simulate processing by adding transformation to list"""
        if transformation not in self.transformations:
            self.transformations.append(transformation)
        self.processed_by.append(transformation)
        self.status = ProcessingStatus.COMPLETED
        return self

    def copy(self) -> 'ImageJob':
        """Create a copy of the job"""
        return ImageJob(
            image_id=self.image_id,
            transformations=self.transformations.copy(),
            current_format=self.current_format,
            panorama_group=self.panorama_group,
            split_into=self.split_into,
            quality_score=self.quality_score,
            correlation_id=self.correlation_id,
            numeric_value=self.numeric_value,
            cycle_count=self.cycle_count,
            iteration_limit=self.iteration_limit,
            is_termination=self.is_termination,
            is_poison_pill=self.is_poison_pill,
            config_updates=self.config_updates.copy() if self.config_updates else None,
            created_at=self.created_at,
            status=self.status,
            processed_by=self.processed_by.copy()
        )

    def __str__(self) -> str:
        return f"ImageJob({self.image_id}, transformations={len(self.transformations)}, format={self.current_format})"