import threading
from queue import Queue, PriorityQueue
from typing import List, Tuple
from .base import SynchronizedNode
from model.image_job import ImageJob

class OrderedProcessingNode(SynchronizedNode):
    """Processes multiple items in parallel but maintains output order"""
    def __init__(self, name: str, worker_count: int = 2):
        super().__init__(name, {"in_0": 1})
        self.worker_count = worker_count
        self.workers: List[threading.Thread] = []
        self.input_queue = Queue()
        self.output_queue = PriorityQueue()  # (sequence, result)
        self.sequence_counter = 0
        self.next_output = 0
        self.output_lock = threading.Lock()
        
    def _run(self):
        """Start workers and output coordinator"""
        # Start worker threads
        for i in range(self.worker_count):
            worker = threading.Thread(
                target=self._worker_func,
                args=(i,),
                name=f"{self.name}_worker_{i}"
            )
            self.workers.append(worker)
            worker.start()
            
        # Output coordinator thread
        coordinator = threading.Thread(
            target=self._output_coordinator,
            name=f"{self.name}_coordinator"
        )
        coordinator.start()
        
        # Main thread feeds input queue
        super()._run()
        
    def _worker_func(self, worker_id: int):
        """Worker processes items from input queue"""
        while self.running:
            try:
                sequence, job = self.input_queue.get(timeout=0.1)
                if job is None:  # Poison pill
                    break
                    
                # Process the job (simulated)
                result = self._process_item(job)
                
                # Put in output queue with sequence
                with self.output_lock:
                    self.output_queue.put((sequence, result))
                    
            except:
                continue
                
    def _output_coordinator(self):
        """Coordinates output to maintain order"""
        buffer = {}
        
        while self.running:
            try:
                # Get next item from output queue
                sequence, result = self.output_queue.get(timeout=0.1)
                buffer[sequence] = result
                
                # Output in order
                while self.next_output in buffer:
                    result = buffer.pop(self.next_output)
                    for output in self.outputs:
                        output.put(result)
                    self.next_output += 1
                    
            except:
                continue
                
    def _process_item(self, job: ImageJob) -> ImageJob:
        """Process single item - override in subclasses"""
        result = job.copy()
        result.add_transformation(f"parallel_processed_by_{self.name}")
        return result
        
    def process(self, inputs):
        """Override to use parallel processing"""
        job = inputs["in_0"][0]
        sequence = self.sequence_counter
        self.sequence_counter += 1
        self.input_queue.put((sequence, job))
        return None  # Output handled by coordinator
        
    def stop(self):
        """Stop all workers"""
        self.running = False
        # Send poison pills to workers
        for _ in range(self.worker_count):
            self.input_queue.put((0, None))
        for worker in self.workers:
            worker.join(timeout=1.0)
        super().stop()