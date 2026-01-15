from typing import Generic, TypeVar, Any, Optional, List
from queue import Queue, Empty
import threading
from model.image_job import ImageJob

T = TypeVar('T')

class Channel(Generic[T]):
    """Statically typed channel for data transmission"""
    def __init__(self, name: str, data_type: type = ImageJob, maxsize: int = 0):
        self.name = name
        self.data_type = data_type
        self.queue = Queue(maxsize=maxsize)
        self.total_put = 0
        self.total_get = 0

    def put(self, item: T, block: bool = True, timeout: Optional[float] = None):
        """Put item into channel with type checking"""
        if not isinstance(item, self.data_type):
            raise TypeError(f"Channel '{self.name}' expects {self.data_type}, got {type(item)}")
        self.queue.put(item, block, timeout)
        self.total_put += 1

    def get(self, block: bool = True, timeout: Optional[float] = None) -> T:
        """Get item from channel"""
        item = self.queue.get(block, timeout)
        self.total_get += 1
        return item

    def empty(self) -> bool:
        return self.queue.empty()

    def size(self) -> int:
        return self.queue.qsize()

    def __str__(self) -> str:
        return f"Channel<{self.data_type.__name__}>('{self.name}', size={self.size()})"

class NodeDSL:
    """Base DSL node definition"""
    def __init__(self, name: str):
        self.name = name
        self.inputs: List[Channel] = []
        self.outputs: List[Channel] = []
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.processed_count = 0

    def add_input(self, channel: Channel) -> 'NodeDSL':
        self.inputs.append(channel)
        return self

    def add_output(self, channel: Channel) -> 'NodeDSL':
        self.outputs.append(channel)
        return self

    def start(self):
        """Start node execution in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._run, name=f"Node-{self.name}")
        self.thread.start()

    def stop(self):
        """Stop node execution"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)

    def _run(self):
        """Main execution loop - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement _run()")

    def process(self, *inputs: Any) -> Any:
        """Processing logic - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement process()")

    def __str__(self) -> str:
        return f"NodeDSL('{self.name}', inputs={len(self.inputs)}, outputs={len(self.outputs)})"

class PipelineDSL:
    """Base pipeline DSL"""
    def __init__(self, name: str):
        self.name = name
        self.nodes: List[NodeDSL] = []
        self.channels: List[Channel] = []

    def add_node(self, node: NodeDSL):
        self.nodes.append(node)
        return self

    def add_channel(self, channel: Channel):
        self.channels.append(channel)
        return self

    def start(self):
        """Start all nodes in the pipeline"""
        for node in self.nodes:
            node.start()

    def stop(self):
        """Stop all nodes in the pipeline"""
        for node in self.nodes:
            node.stop()

    def __str__(self) -> str:
        return f"PipelineDSL('{self.name}', nodes={len(self.nodes)}, channels={len(self.channels)})"