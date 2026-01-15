"""
All node types for the pipeline system
"""

# Import each module individually to avoid circular imports
import dsl.nodes.base as base
import dsl.nodes.filters as filters
import dsl.nodes.configurable as configurable
import dsl.nodes.parallel as parallel

# Re-export with clear names
SynchronizedNode = base.SynchronizedNode

# 5 Filter types
OneToOneNode = filters.OneToOneNode
TypeTransformNode = filters.TypeTransformNode
NToOneNode = filters.NToOneNode
OneToNNode = filters.OneToNNode
SelectionNode = filters.SelectionNode
SummatorNode = filters.SummatorNode

# Advanced nodes
ConfigurableNode = configurable.ConfigurableNode
ConfigurableBlurNode = configurable.ConfigurableBlurNode
OrderedProcessingNode = parallel.OrderedProcessingNode

__all__ = [
    'SynchronizedNode',
    'OneToOneNode', 'TypeTransformNode', 'NToOneNode',
    'OneToNNode', 'SelectionNode', 'SummatorNode',
    'ConfigurableNode', 'ConfigurableBlurNode',
    'OrderedProcessingNode'
]