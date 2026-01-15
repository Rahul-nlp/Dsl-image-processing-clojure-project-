"""
Domain-Specific Language for Photo Processing Pipelines
All DSL functions are exported here for clean user interface
"""

# DSL Core
from .core import Channel, NodeDSL, PipelineDSL

# DSL API functions (these are the actual DSL)
from .dsl_api import (
    # Pipeline creation
    pipeline, with_cycles, monitored_pipeline,
    
    # Node creation
    node, source, sink,
    
    # Filter factories (5 types)
    blur, convert, stitch, split, select_best, summator,
    
    # Advanced nodes
    configurable, parallel,
    
    # Connection
    connect
)

__all__ = [
    # Core types (for advanced use)
    'Channel', 'NodeDSL', 'PipelineDSL',
    
    # DSL API (this is what users use)
    'pipeline', 'with_cycles', 'monitored_pipeline',
    'node', 'source', 'sink',
    'blur', 'convert', 'stitch', 'split', 'select_best', 'summator',
    'configurable', 'parallel',
    'connect'
]