import threading
import time
from typing import Dict, List, Optional
from .core import PipelineDSL, Channel

class PipelineMonitor:
    """Monitors pipeline health and activity"""
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.pipeline: Optional[PipelineDSL] = None
        self.metrics: Dict[str, List[float]] = {
            'channel_sizes': [],
            'node_activity': [],
            'throughput': []
        }

    def attach_pipeline(self, pipeline: PipelineDSL):
        """Attach pipeline to monitor"""
        self.pipeline = pipeline

    def start(self):
        """Start monitoring"""
        if not self.pipeline:
            raise ValueError("No pipeline attached")

        self.running = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            name="PipelineMonitor"
        )
        self.monitor_thread.start()
        print(f"📊 Pipeline monitor started (interval: {self.interval}s)")

    def stop(self):
        """Stop monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.running and self.pipeline:
            # Collect metrics
            total_size = sum(channel.size() for channel in self.pipeline.channels)
            active_nodes = sum(1 for node in self.pipeline.nodes if node.running)

            self.metrics['channel_sizes'].append(total_size)
            self.metrics['node_activity'].append(active_nodes)

            # Check for potential issues
            if total_size > 100:  # Arbitrary threshold
                print(f"⚠️  High backlog: {total_size} items in channels")

            if active_nodes == 0 and total_size > 0:
                print("⚠️  No active nodes but channels have data")

            time.sleep(self.interval)

    def print_report(self):
        """Print monitoring report"""
        if not self.metrics['channel_sizes']:
            print("No monitoring data available")
            return

        print("\n📈 PIPELINE MONITORING REPORT")
        print("-" * 40)
        print(f"Avg channel size: {sum(self.metrics['channel_sizes'])/len(self.metrics['channel_sizes']):.1f}")
        print(f"Max channel size: {max(self.metrics['channel_sizes'])}")
        print(f"Avg active nodes: {sum(self.metrics['node_activity'])/len(self.metrics['node_activity']):.1f}")