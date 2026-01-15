import threading
import time
from ..core import PipelineDSL
from ..monitoring import PipelineMonitor

class CompletionAwarePipeline(PipelineDSL):
    """Pipeline with completion detection and timeout"""
    def __init__(self, name: str, timeout: float = 30.0):
        super().__init__(name)
        self.timeout = timeout
        self.start_time = None  # type: float | None
        self.end_time = None    # type: float | None
        self.completed = False
        self.completion_event = threading.Event()
        self.monitor = None     # type: PipelineMonitor | None
        self.timeout_thread = None  # type: threading.Thread | None
        
    def start(self):
        """Start pipeline with monitoring"""
        self.start_time = time.time()
        self.completed = False
        
        # Start timeout monitor
        self.timeout_thread = threading.Thread(
            target=self._timeout_monitor,
            name=f"{self.name}_timeout_monitor"
        )
        self.timeout_thread.start()
        
        # Start monitor if configured
        if self.monitor:
            self.monitor.start()
            
        super().start()
        
    def _timeout_monitor(self):
        """Monitor for timeout"""
        while not self.completion_event.is_set():
            elapsed = time.time() - (self.start_time or 0)
            if elapsed > self.timeout:
                print(f"⏰ TIMEOUT: Pipeline '{self.name}' exceeded {self.timeout}s")
                self._diagnose_stuck()
                self.completion_event.set()
                break
            time.sleep(0.1)
            
    def _diagnose_stuck(self):
        """Diagnose why pipeline is stuck"""
        print(f"\n🔍 DIAGNOSING PIPELINE '{self.name}':")
        
        # Check node activity
        active_nodes = sum(1 for node in self.nodes if node.running)
        print(f"  Active nodes: {active_nodes}/{len(self.nodes)}")
        
        # Check channel states
        for channel in self.channels:
            if channel.size() > 10:  # Arbitrary threshold
                print(f"  Channel '{channel.name}' has {channel.size()} pending items")
                
        # Check for cycles
        if hasattr(self, 'cycles'):
            for cycle in self.cycles:
                print(f"  Cycle '{cycle.get('description', 'unnamed')}': "
                      f"iterations={cycle.get('iteration_count', 0)}")
                      
    def wait_for_completion(self, timeout=None):
        """Wait for pipeline completion"""
        timeout = timeout or self.timeout
        result = self.completion_event.wait(timeout)
        
        if result:
            self.completed = True
            self.end_time = time.time()
            print(f"✅ Pipeline '{self.name}' completed in {self.end_time - self.start_time:.2f}s")
        else:
            print(f"⚠️ Pipeline '{self.name}' did not complete in {timeout}s")
            
        return result
        
    def attach_monitor(self, monitor):
        """Attach a pipeline monitor"""
        self.monitor = monitor
        self.monitor.attach_pipeline(self)
        
    def stop(self):
        """Stop pipeline and cleanup"""
        self.completion_event.set()
        if self.timeout_thread:
            self.timeout_thread.join(timeout=1.0)
        if self.monitor:
            self.monitor.stop()
        super().stop()