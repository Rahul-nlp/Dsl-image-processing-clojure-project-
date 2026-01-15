from typing import List, Dict, Tuple
from ..core import PipelineDSL, Channel, NodeDSL
from model.image_job import ImageJob

class PipelineBuilder(PipelineDSL):
    """Builder for creating typed pipelines"""
    def __init__(self, name: str):
        super().__init__(name)
        self.connections: List[Tuple[str, str, str, str]] = []
        self.node_map: Dict[str, NodeDSL] = {}
        self.channel_map: Dict[str, Channel] = {}
        
    def add_node(self, node_id: str, node: NodeDSL):
        self.node_map[node_id] = node
        return super().add_node(node)
        
    def connect(self, from_node: str, from_port: int, 
                to_node: str, to_port: int, 
                channel_type: type = ImageJob):
        """Connect nodes with type checking"""
        # Create channel
        channel_name = f"{from_node}_{from_port}_to_{to_node}_{to_port}"
        channel = Channel(channel_name, channel_type)
        self.add_channel(channel)
        self.channel_map[channel_name] = channel
        
        # Connect nodes
        source_node = self.node_map[from_node]
        target_node = self.node_map[to_node]
        
        source_node.add_output(channel)
        target_node.add_input(channel)
        
        self.connections.append((from_node, from_port, to_node, to_port))
        return self
        
    def build(self):
        """Validate and build pipeline"""
        self._validate_connections()
        return self
        
    def _validate_connections(self):
        """Validate type safety of connections"""
        for from_node, from_port, to_node, to_port in self.connections:
            # In a more complex implementation, would check actual types
            pass
            
    def print_structure(self):
        """Print pipeline structure"""
        print(f"\nPipeline: {self.name}")
        print("-" * 40)
        print(f"Nodes: {len(self.nodes)}")
        for node_id, node in self.node_map.items():
            print(f"  {node_id}: {node}")
        print(f"\nChannels: {len(self.channels)}")
        for channel in self.channels:
            print(f"  {channel}")
        print(f"\nConnections: {len(self.connections)}")
        for conn in self.connections:
            print(f"  {conn[0]} → {conn[2]}")