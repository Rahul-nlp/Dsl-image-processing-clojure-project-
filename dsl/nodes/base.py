import threading
import time
from typing import List, Dict, Any, Optional
from collections import defaultdict
from ..core import NodeDSL, Channel
from model.image_job import ImageJob

class SynchronizedNode(NodeDSL):
    """Node that waits for specific input patterns (professor's requirement)"""
    def __init__(self, name: str, input_requirements: Dict[str, int] = None):
        """
        input_requirements: {"input_port": count} - how many items needed from each port
        Example: {"in1": 1, "in2": 1} = summator needs 1 from each
        """
        super().__init__(name)
        self.input_requirements = input_requirements or {"default": 1}
        self.input_buffers = defaultdict(list)
        self.buffer_locks = defaultdict(threading.Lock)
        self.verbose = False
        
    def _wait_for_inputs(self) -> Dict[str, List[ImageJob]]:
        """Wait until all required inputs are available (professor's synchronization)"""
        while self.running:
            ready_inputs = {}
            all_ready = True
            
            for port_idx, channel in enumerate(self.inputs):
                port_name = f"in_{port_idx}"
                required = self.input_requirements.get(port_name, 1)
                
                with self.buffer_locks[port_name]:
                    if len(self.input_buffers[port_name]) < required:
                        # Not enough data in this buffer
                        try:
                            # Try to get more data
                            item = channel.get(timeout=0.1)
                            self.input_buffers[port_name].append(item)
                        except:
                            all_ready = False
                            break
                    
                    # Check again after potential get
                    if len(self.input_buffers[port_name]) >= required:
                        ready_inputs[port_name] = self.input_buffers[port_name][:required]
                        # Remove consumed items
                        self.input_buffers[port_name] = self.input_buffers[port_name][required:]
                    else:
                        all_ready = False
                        break
            
            if all_ready:
                if self.verbose:
                    print(f"[{self.name}] Got all required inputs: {ready_inputs}")
                return ready_inputs
            else:
                time.sleep(0.01)  # Yield to avoid busy waiting
        
        return {}
    
    def _run(self):
        """Main execution with synchronization"""
        while self.running:
            try:
                # Wait for required inputs (professor's synchronization requirement)
                inputs = self._wait_for_inputs()
                if not inputs:
                    continue
                    
                # Process the inputs
                result = self.process(inputs)
                self.processed_count += 1
                
                # Send to outputs
                if result:
                    if isinstance(result, list):
                        for item in result:
                            for output in self.outputs:
                                output.put(item)
                    else:
                        for output in self.outputs:
                            output.put(result)
                            
            except Exception as e:
                if self.verbose:
                    print(f"[{self.name}] Error: {e}")
                    
    def set_verbose(self, verbose: bool):
        self.verbose = verbose
        return self