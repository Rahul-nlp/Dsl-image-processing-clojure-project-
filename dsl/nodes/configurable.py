import threading
from .base import SynchronizedNode

class ConfigurableNode(SynchronizedNode):
    """Node with runtime-configurable parameters"""
    def __init__(self, name: str):
        super().__init__(name)
        self.config = {}
        self.config_lock = threading.RLock()
        
    def set_config(self, **kwargs):
        """Set configuration parameters"""
        with self.config_lock:
            old_config = self.config.copy()
            self.config.update(kwargs)
            print(f"[{self.name}] Config updated: {kwargs}")
            self._on_config_change(old_config, self.config)
        return self
        
    def get_config(self, key: str, default=None):
        """Get configuration value"""
        with self.config_lock:
            return self.config.get(key, default)
            
    def _on_config_change(self, old_config, new_config):
        """Called when configuration changes - override in subclasses"""
        pass

class ConfigurableBlurNode(ConfigurableNode):
    """Configurable blur filter"""
    def __init__(self, name: str):
        super().__init__(name)
        self.set_config(radius=2.0, intensity=1.0, method="gaussian")
        
    def process(self, inputs):
        # Import here to avoid circular imports
        from model.image_job import ImageJob
        
        job = inputs["in_0"][0].copy()
        radius = self.get_config("radius", 2.0)
        intensity = self.get_config("intensity", 1.0)
        method = self.get_config("method", "gaussian")
        job.add_transformation(f"blur_{method}_r{radius}_i{intensity}")
        return job