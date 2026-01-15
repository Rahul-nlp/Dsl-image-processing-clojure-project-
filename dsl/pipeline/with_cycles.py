from typing import Dict, Any, Callable, Optional, List
from ..core import PipelineDSL, Channel
from model.image_job import ImageJob

class PipelineWithCycles(PipelineDSL):
    """Pipeline supporting feedback loops/cycles"""
    def __init__(self, name: str):
        super().__init__(name)
        self.cycles: List[Dict[str, Any]] = []
        
    def add_cycle(self, from_node: str, to_node: str, 
                  max_iterations: int = 10,
                  condition: Optional[Callable[[ImageJob], bool]] = None,
                  description: str = ""):
        """Add a feedback cycle with safety limits"""
        if max_iterations <= 0:
            raise ValueError("max_iterations must be > 0 to prevent infinite loops")
            
        cycle = {
            "from_node": from_node,
            "to_node": to_node,
            "max_iterations": max_iterations,
            "condition": condition,
            "description": description,
            "iteration_count": 0
        }
        self.cycles.append(cycle)
        return self
        
    def _process_with_cycle(self, job: ImageJob, cycle_id: int) -> ImageJob:
        """Process job through a cycle"""
        cycle = self.cycles[cycle_id]
        
        # Check iteration limit
        if job.cycle_count >= cycle["max_iterations"]:
            print(f"⚠️ Cycle limit reached for {job.image_id}")
            return job
            
        # Check condition
        if cycle["condition"] and not cycle["condition"](job):
            return job
            
        # Increment cycle count
        result = job.copy()
        result.cycle_count += 1
        result.add_transformation(f"cycle_{cycle_id}_iteration_{result.cycle_count}")
        
        cycle["iteration_count"] += 1
        
        return result
        
    def _detect_deadlock(self) -> bool:
        """Detect potential deadlocks in cycles"""
        for cycle in self.cycles:
            if cycle["iteration_count"] > cycle["max_iterations"] * 100:
                # Excessive iterations suggest deadlock
                print(f"🚨 DEADLOCK DETECTED in cycle {cycle['description']}")
                print(f"   Iterations: {cycle['iteration_count']}, Max: {cycle['max_iterations']}")
                return True
        return False