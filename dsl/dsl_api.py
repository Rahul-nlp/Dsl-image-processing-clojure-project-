"""
Domain-Specific Language API
Provides a clean, declarative interface for building pipelines
"""
import time

# Import everything at module level for clean DSL
from .pipeline.builder import PipelineBuilder
from .pipeline.with_cycles import PipelineWithCycles
from .pipeline.completion import CompletionAwarePipeline

from .nodes.base import SynchronizedNode
from .nodes.filters import (
    OneToOneNode, TypeTransformNode, NToOneNode,
    OneToNNode, SelectionNode, SummatorNode
)
from .nodes.configurable import ConfigurableBlurNode
from .nodes.parallel import OrderedProcessingNode

# ============ DSL ENTRY POINTS ============

def pipeline(name: str, timeout: float = 30.0) -> PipelineBuilder:
    """Start a new pipeline definition - DSL entry point"""
    return PipelineBuilder(name)

def with_cycles(name: str) -> PipelineWithCycles:
    """Create a pipeline that supports cycles - DSL"""
    return PipelineWithCycles(name)

def monitored_pipeline(name: str, timeout: float = 30.0) -> CompletionAwarePipeline:
    """Create a pipeline with completion detection - DSL"""
    return CompletionAwarePipeline(name, timeout)

def node(name: str):
    """Create a node builder - DSL for node creation"""
    class NodeBuilder:
        def __init__(self, node_name: str):
            self.name = node_name

        def of_type(self, node_type: str, **kwargs):
            """Specify node type - part of DSL syntax"""
            if node_type == "1-to-1":
                return OneToOneNode(self.name, kwargs.get('operation', 'transform'))
            elif node_type == "type":
                return TypeTransformNode(self.name, kwargs.get('target_format', 'JPG'))
            elif node_type == "n-to-1":
                return NToOneNode(self.name, kwargs.get('group_size', 3))
            elif node_type == "1-to-n":
                return OneToNNode(self.name)
            elif node_type == "selection":
                return SelectionNode(self.name, kwargs.get('num_inputs', 2))
            elif node_type == "summator":
                return SummatorNode(self.name)
            else:
                raise ValueError(f"Unknown node type: {node_type}")

    return NodeBuilder(name)

def source(data: list, name: str = "source") -> 'SourceNode': # type: ignore
    """Create a source node - DSL"""
    class SourceNode(SynchronizedNode):
        def __init__(self, node_name: str, data_list: list):
            super().__init__(node_name, {"in_0": 0})
            self.data = data_list
            self.index = 0

        def _run(self):
            while self.running and self.index < len(self.data):
                item = self.data[self.index]
                for output in self.outputs:
                    output.put(item)
                self.index += 1
                time.sleep(0.01)
            self.running = False

    return SourceNode(name, data)

def sink(name: str = "sink") -> 'SinkNode': # type: ignore
    class SinkNode(SynchronizedNode):
        def __init__(self, node_name: str):
            super().__init__(node_name, {"in_0": 1, "in_1": 1})
            self.received = []

        def process(self, inputs):
            from model.image_job import ImageJob

            # Handle real data
            if "in_0" in inputs:
                job = inputs["in_0"][0]
                if not job.is_termination:
                    self.received.append(job)
                    print(f"[{self.name}] Received: {job.image_id} with transformations: {job.transformations}")

            # Handle termination
            if "in_1" in inputs:
                term = inputs["in_1"][0]
                if term.is_termination:
                    print(f"[{self.name}] Termination signal received. Stopping pipeline.")
                    self.running = False

            return None

    return SinkNode(name)


def connect(pipeline_builder, from_node: str, from_port: int,
            to_node: str, to_port: int):
    """Connect nodes - DSL for pipeline wiring"""
    return pipeline_builder.connect(from_node, from_port, to_node, to_port)

# ============ FILTER FACTORIES (5 Types) ============

def blur(name: str = "blur", radius: float = 2.0) -> ConfigurableBlurNode:
    """1-to-1 transformation DSL: blur filter"""
    node = ConfigurableBlurNode(name)
    node.set_config(radius=radius)
    return node

def convert(name: str = "convert", target_format: str = "JPG") -> TypeTransformNode:
    """Type transformation DSL: format conversion"""
    return TypeTransformNode(name, target_format)

def stitch(name: str = "stitch", group_size: int = 3) -> NToOneNode:
    """n-to-1 transformation DSL: panorama stitching"""
    return NToOneNode(name, group_size)

def split(name: str = "split") -> OneToNNode:
    """1-to-n transformation DSL: image splitting"""
    return OneToNNode(name)

def select_best(name: str = "selector", num_inputs: int = 2) -> SelectionNode:
    """1-of-n selection DSL: choose best result"""
    return SelectionNode(name, num_inputs)

def summator(name: str = "summator") -> SummatorNode:
    """Professor's example DSL: summator node"""
    return SummatorNode(name)

# ============ ADVANCED NODES DSL ============

def configurable(name: str = "configurable") -> ConfigurableBlurNode:
    """Configurable node DSL"""
    return ConfigurableBlurNode(name)

def parallel(name: str = "parallel", workers: int = 2) -> OrderedProcessingNode:
    """Parallel processing node DSL"""
    return OrderedProcessingNode(name, workers)