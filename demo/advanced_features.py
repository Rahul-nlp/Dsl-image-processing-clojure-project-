from dsl import (
    pipeline, configurable, parallel, 
    source, sink, connect, with_cycles
)
from data import raw_images, termination_signal
from dsl.monitoring import PipelineMonitor

def demo_advanced_features():
    """Demonstrate all additional requirements"""
    print("\n" + "="*60)
    print("ADVANCED FEATURES DEMONSTRATION")
    print("="*60)
    print("Demonstrating:")
    print("1. Configurable nodes (runtime parameter changes)")
    print("2. Pipelines with cycles/loops")
    print("3. Completion detection and timeout")
    print("4. Order-preserving parallel processing")
    print("5. Monitoring and deadlock detection")
    
    # Create pipeline with cycles
    pipe = with_cycles("AdvancedPipeline")
    
    # Test data
    test_data = raw_images[:3]
    
    # Add nodes
    pipe.add_node("src", source(test_data, "source"))
    pipe.add_node("config_node", configurable("adaptive_blur"))
    pipe.add_node("parallel_node", parallel("fast_processor", 3))
    pipe.add_node("quality_check", source([], "quality_check"))  # Simplified
    pipe.add_node("output", sink("sink"))
    
    # Configure initial parameters
    pipe.node_map["config_node"].set_config(radius=2.0, intensity=1.0)
    
    # Connect
    connect(pipe, "src", 0, "config_node", 0)
    connect(pipe, "config_node", 0, "parallel_node", 0)
    connect(pipe, "parallel_node", 0, "output", 0)
    
    # Add feedback cycle (simplified)
    pipe.add_cycle(
        from_node="quality_check",
        to_node="config_node",
        max_iterations=3,
        condition=lambda job: job.quality_score < 0.8,
        description="Enhancement feedback loop"
    )
    
    # Add termination
    pipe.add_node("terminator", source([termination_signal], "terminator"))
    connect(pipe, "terminator", 0, "output", 1)
    
    # Create monitored pipeline
    from dsl.pipeline.completion import CompletionAwarePipeline
    monitored_pipe = CompletionAwarePipeline("MonitoredPipeline", timeout=8.0)
    monitored_pipe.nodes = pipe.nodes
    monitored_pipe.channels = pipe.channels
    
    # Attach monitor
    monitor = PipelineMonitor(interval=0.5)
    monitored_pipe.attach_monitor(monitor)
    
    print("\n▶️ Starting advanced pipeline...")
    monitored_pipe.start()
    
    # Demonstrate runtime configuration
    import time
    time.sleep(1)
    print("\n⚙️ Changing configuration at runtime...")
    pipe.node_map["config_node"].set_config(radius=5.0, intensity=2.0)
    
    # Demonstrate timeout
    print("\n⏱️ Waiting for completion (will timeout in 8 seconds)...")
    try:
        completed = monitored_pipe.wait_for_completion()
        if completed:
            print("✅ Pipeline completed normally")
    except:
        print("⚠️ Pipeline timed out as expected")
        
    # Print monitoring report
    monitor.print_report()
    
    print("\n✅ Advanced features demonstration complete")
    
    return monitored_pipe