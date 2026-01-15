from typing import List, Dict, Any
from collections import defaultdict
from ..core import Channel
from .base import SynchronizedNode

# Note: ImageJob is imported inside methods to avoid circular imports

# ============ Source Node ============
class SourceNode(SynchronizedNode):
    """Source node that produces data"""
    def __init__(self, name: str):
        super().__init__(name, {})  # No inputs for source node
        self.data_queue = []
        
    def add_data(self, data: Any):
        """Add data to be processed by this source node"""
        self.data_queue.append(data)
        
    def process(self, inputs: Dict[str, List]) -> Any:
        # Source nodes don't have inputs, they produce from internal queue
        if self.data_queue:
            return self.data_queue.pop(0)
        return None

# ============ Sink Node ============
class SinkNode(SynchronizedNode):
    """Sink node that consumes data"""
    def __init__(self, name: str):
        super().__init__(name, {"in_0": 1})
        
    def process(self, inputs: Dict[str, List]) -> Any:
        from model.image_job import ImageJob  # Import here
        job = inputs["in_0"][0]
        # Sink nodes typically don't return data, but we can log/process it
        print(f"[{self.name}] Received: {job.image_id} with transformations: {job.transformations}")
        return None  # Sink nodes typically don't produce output

# ============ 1-to-1 Transformation ============
class OneToOneNode(SynchronizedNode):
    """1-to-1 transformation: blur, noise reduction, etc."""
    def __init__(self, name: str, operation: str):
        super().__init__(name, {"in_0": 1})
        self.operation = operation
        
    def process(self, inputs: Dict[str, List]) -> Any:
        from model.image_job import ImageJob  # Import here to avoid circular import
        job = inputs["in_0"][0].copy()
        job.add_transformation(self.operation)
        return job

# ============ Type Transformation ============
class TypeTransformNode(SynchronizedNode):
    """Type transformation: PNG→JPG, etc."""
    def __init__(self, name: str, target_format: str):
        super().__init__(name, {"in_0": 1})
        self.target_format = target_format
        
    def process(self, inputs: Dict[str, List]) -> Any:
        from model.image_job import ImageJob  # Import here
        job = inputs["in_0"][0].copy()
        old_format = job.current_format
        job.current_format = self.target_format
        job.add_transformation(f"convert_{old_format}_to_{self.target_format}")
        return job

# ============ n-to-1 Transformation ============
class NToOneNode(SynchronizedNode):
    """n-to-1 transformation: panorama stitching, HDR"""
    def __init__(self, name: str, group_size: int = 3):
        super().__init__(name, {"in_0": group_size})
        self.group_size = group_size
        self.pending_groups = {}
        
    def process(self, inputs: Dict[str, List]) -> Any:
        from model.image_job import ImageJob  # Import here
        jobs = inputs["in_0"]
        
        # Group by panorama_group if present
        panorama_group = None
        for job in jobs:
            if hasattr(job, 'panorama_group') and job.panorama_group:
                panorama_group = job.panorama_group
                break
                
        if panorama_group:
            # Create stitched panorama
            result = ImageJob(
                image_id=f"{panorama_group}_panorama",
                transformations=["loaded", "stitched"],
                current_format=jobs[0].current_format,
                quality_score=sum(getattr(j, 'quality_score', 0) or 0 for j in jobs) / len(jobs)
            )
        else:
            # Generic n-to-1 operation
            result = ImageJob(
                image_id=f"merged_{self.processed_count}",
                transformations=["loaded", "merged"],
                current_format=jobs[0].current_format,
                quality_score=sum(getattr(j, 'quality_score', 0) or 0 for j in jobs) / len(jobs)
            )
            
        return result

# ============ 1-to-n Transformation ============
class OneToNNode(SynchronizedNode):
    """1-to-n transformation: splitting into regions"""
    def __init__(self, name: str):
        super().__init__(name, {"in_0": 1})
        
    def process(self, inputs: Dict[str, List]) -> List[Any]:
        from model.image_job import ImageJob  # Import here
        job = inputs["in_0"][0]
        split_count = getattr(job, 'split_into', 2) or 2
        
        results = []
        for i in range(split_count):
            split_job = job.copy()
            split_job.image_id = f"{job.image_id}_part_{i+1}"
            split_job.add_transformation(f"split_part_{i+1}")
            if hasattr(split_job, 'split_into'):
                split_job.split_into = None  # Reset for downstream
            results.append(split_job)
            
        return results

# ============ 1-of-n Selection ============
class SelectionNode(SynchronizedNode):
    """Selection of one out of n: compare results, choose best"""
    def __init__(self, name: str, num_inputs: int = 2):
        input_reqs = {f"in_{i}": 1 for i in range(num_inputs)}
        super().__init__(name, input_reqs)
        self.num_inputs = num_inputs
        self.correlation_buffers = defaultdict(list)
        
    def process(self, inputs: Dict[str, List]) -> Any:
        from model.image_job import ImageJob  # Import here
        
        # Collect all inputs
        all_jobs = []
        for port_jobs in inputs.values():
            all_jobs.extend(port_jobs)
            
        # Group by correlation_id
        groups = defaultdict(list)
        for job in all_jobs:
            if hasattr(job, 'correlation_id') and job.correlation_id:
                groups[job.correlation_id].append(job)
                
        # Process first complete group
        for corr_id, jobs in groups.items():
            if len(jobs) >= self.num_inputs:
                # Select best by quality score
                best_job = max(jobs, key=lambda j: getattr(j, 'quality_score', 0) or 0)
                result = best_job.copy()
                result.add_transformation(f"selected_best_from_{len(jobs)}")
                if hasattr(result, 'correlation_id'):
                    result.correlation_id = None  # Clear for downstream
                return result
                
        # If no complete group, return first job
        if all_jobs:
            return all_jobs[0].copy()
        return None

# ============ Professor's Summator Example ============
class SummatorNode(SynchronizedNode):
    """Professor's example: summator with two inputs, one output"""
    def __init__(self, name: str):
        super().__init__(name, {"in_0": 1, "in_1": 1})
        
    def process(self, inputs: Dict[str, List]) -> Any:
        from model.image_job import ImageJob  # Import here
        
        # Get one from each input channel
        job1 = inputs["in_0"][0]
        job2 = inputs["in_1"][0]
        
        # Sum numeric values (if present)
        value1 = getattr(job1, 'numeric_value', 0) or 0
        value2 = getattr(job2, 'numeric_value', 0) or 0
        total = value1 + value2
        
        # Create result
        result = ImageJob(
            image_id=f"sum_{self.processed_count}",
            transformations=["summation"],
            numeric_value=total,
            current_format=getattr(job1, 'current_format', '')
        )
        
        # Demonstrate accumulation warning
        leftover1 = len(self.input_buffers.get("in_0", []))
        leftover2 = len(self.input_buffers.get("in_1", []))
        if leftover1 > 0 or leftover2 > 0:
            print(f"⚠️ [{self.name}] Data accumulation: in_0={leftover1}, in_1={leftover2}")
        return result