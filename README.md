"# Dsl-image-processing-clojure-project-" 

-------------------------------------------
   Ruslan and Rahul 
------------------------------------------
       
 ✅ DSL imported successfully - clean, declarative interface
   No implementation details exposed to user

   ✓ Clean, readable syntax
   ✓ Hides threading/channel complexity
Simple photo processing pipeline


 5 FILTER TYPES FOR PHOTO PROCESSING (Model Task):
    ✓ 1-to-1: noise_reduction
    ✓ type: format_converter
    ✓ n-to-1: panorama_stitcher
    ✓ 1-to-n: image_splitter
    ✓ 1-of-n: best_selector

 STATIC TYPING OF CHANNELS (Type safety):
   ✓ Channel<ImageJob> enforces type safety
   ✓ Prevents incorrect data types in pipeline

PARALLEL EXECUTION (Multithreaded nodes):
   Created: fast_processor with 3 worker threads
   ✓ Processes multiple photos simultaneously
   ✓ Maintains output order (professor's requirement)

Additional 
   ✓ Configurable nodes: runtime parameter changes
   ✓ Pipelines with cycles/feedback loops
   ✓ Completion detection with timeout
   ✓ Diagnoses stuck pipelines (deadlock detection)


What i did 

  ✓ DSL for pipeline schemes
   ✓ Nodes with I/O channels
   ✓ Static typing of channels
   ✓ Pipeline formation with typing
   ✓ Pipeline execution & processing
   ✓ Parallel node execution
   ✓ Reuse of identical nodes
   ✓ 5 filter types (model task)
   ✓ Configurable nodes at runtime
   ✓ Pipelines with cycles
   ✓ Completion detection
   ✓ Order-preserving multithreading
   ✓ Professor's summator example


This file exposes the clean DSL interface. Users import pipeline, blur, stitch, connect, etc. without seeing implementation details  Clean DSL, no implementation leakage
            Dsl_api  → Core → base → filter ->configurable →parallel →builder→cycles→completion → monitoring(deadlock)
