from dsl import pipeline, node, source, sink, connect
from data import raw_images

def demo_basic_dsl():
    """Demonstrate basic DSL usage"""
    print("\n" + "="*60)
    print("BASIC DSL DEMONSTRATION")
    print("="*60)
    
    # Create pipeline using DSL
    pipe = pipeline("BasicPipeline", timeout=10.0)
    
    # Add nodes
    pipe.add_node("src", source(raw_images, "source"))
    pipe.add_node("transform", node("blur").of_type("1-to-1", operation="blur"))
    pipe.add_node("output", sink("sink"))
    
    # Connect nodes
    connect(pipe, "src", 0, "transform", 0)
    connect(pipe, "transform", 0, "output", 0)
    
    # Build and execute
    pipe.build()
    pipe.print_structure()
    
    print("\n▶️ Starting pipeline...")
    pipe.start()
    
    import time
    time.sleep(2)
    
    print("\n⏹️ Stopping pipeline...")
    pipe.stop()
    
    print("\n✅ Basic DSL demonstration complete")
    
    return pipe