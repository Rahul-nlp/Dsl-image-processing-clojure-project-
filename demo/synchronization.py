from dsl import pipeline, summator, source, sink, connect
from model.image_job import ImageJob

def demo_synchronization():
    """Demonstrate professor's summator example and synchronization issues"""
    print("\n" + "="*60)
    print("SYNCHRONIZATION DEMONSTRATION (Professor's Example)")
    print("="*60)
    
    # Create test data that demonstrates synchronization
    unbalanced_data_a = [
        ImageJob(image_id="A1", numeric_value=1),
        ImageJob(image_id="A2", numeric_value=2),
        ImageJob(image_id="A3", numeric_value=3),
        ImageJob(image_id="A4", numeric_value=4),
        ImageJob(image_id="A5", numeric_value=5),
    ]
    
    unbalanced_data_b = [
        ImageJob(image_id="B1", numeric_value=10),
        ImageJob(image_id="B2", numeric_value=20),
    ]
    
    print("\n📊 Test scenario:")
    print("Channel A: 5 items (1, 2, 3, 4, 5)")
    print("Channel B: 2 items (10, 20)")
    print("\nExpected behavior:")
    print("1. Summator processes: (1 + 10) = 11")
    print("2. Summator processes: (2 + 20) = 22") 
    print("3. Channel A has 3 remaining items (3, 4, 5)")
    print("4. These WAIT forever for matching inputs from Channel B")
    print("   ⚠️ This demonstrates 'data accumulation' problem")
    
    # Create pipeline
    pipe = pipeline("SynchronizationDemo", timeout=5.0)
    
    # Add nodes
    pipe.add_node("source_a", source(unbalanced_data_a, "source_a"))
    pipe.add_node("source_b", source(unbalanced_data_b, "source_b"))
    pipe.add_node("summer", summator("summator").set_verbose(True))
    pipe.add_node("output", sink("sink"))
    
    # Connect
    connect(pipe, "source_a", 0, "summer", 0)
    connect(pipe, "source_b", 0, "summer", 1)
    connect(pipe, "summer", 0, "output", 0)
    
    pipe.build()
    
    print("\n▶️ Running synchronization demo...")
    pipe.start()
    
    try:
        pipe.wait_for_completion(4.0)
    except:
        print("\n⚠️ Pipeline timed out (expected due to unbalanced inputs)")
        print("✅ This demonstrates the synchronization issue!")
        
    return pipe