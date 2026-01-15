from dsl import (
    pipeline, blur, convert, stitch, split, select_best,
    source, sink, connect, parallel
)
from data import (
    raw_images, panorama_parts, split_input,
    selection_variants, termination_signal
)


def demo_model_task():
    """Demonstrate complete model task with all 5 filter types"""

    print("\n" + "=" * 60)
    print("COMPLETE MODEL TASK DEMONSTRATION")
    print("=" * 60)
    print("Demonstrating all 5 filter types:")
    print("1. 1-to-1: Blur")
    print("2. Type: PNG→JPG conversion")
    print("3. n-to-1: Panorama stitching")
    print("4. 1-to-n: Image splitting")
    print("5. 1-of-n: Best noise reduction selection")

    # --------------------------------------------------
    # 1. Prepare test data
    # --------------------------------------------------
    test_data = raw_images[:2] + panorama_parts + [split_input] + selection_variants

    # --------------------------------------------------
    # 2. BUILD pipeline using PipelineBuilder (DSL)
    # --------------------------------------------------
    pipe = pipeline("ModelTaskPipeline", timeout=20.0)

    pipe.add_node("src", source(test_data, "source"))
    pipe.add_node("blur1", blur("blur_small", 1.5))
    pipe.add_node("blur2", blur("blur_large", 3.0))
    pipe.add_node("selector", select_best("best_selector", 2))
    pipe.add_node("stitcher", stitch("panorama_stitcher", 3))
    pipe.add_node("splitter", split("image_splitter"))
    pipe.add_node("parallel_proc", parallel("parallel_processor", 2))
    pipe.add_node("converter", convert("format_converter", "JPG"))
    pipe.add_node("output", sink("final_sink"))

    # termination signal
    pipe.add_node("terminator", source([termination_signal], "terminator"))

    # --------------------------------------------------
    # 3. Connect nodes (DSL)
    # --------------------------------------------------
    connect(pipe, "src", 0, "blur1", 0)
    connect(pipe, "src", 1, "blur2", 0)
    connect(pipe, "blur1", 0, "selector", 0)
    connect(pipe, "blur2", 0, "selector", 1)
    connect(pipe, "selector", 0, "stitcher", 0)
    connect(pipe, "stitcher", 0, "splitter", 0)
    connect(pipe, "splitter", 0, "parallel_proc", 0)
    connect(pipe, "parallel_proc", 0, "converter", 0)
    connect(pipe, "converter", 0, "output", 0)
    connect(pipe, "terminator", 0, "output", 1)

    pipe.build()
    pipe.print_structure()

    # --------------------------------------------------
    # 4. EXECUTE with CompletionAwarePipeline (FIX)
    # --------------------------------------------------
    print("\n▶️ Executing model task pipeline...")

    from dsl.pipeline.completion import CompletionAwarePipeline

    exec_pipe = CompletionAwarePipeline("ModelTaskPipeline", timeout=20.0)
    exec_pipe.nodes = pipe.nodes
    exec_pipe.channels = pipe.channels

    import time

    exec_pipe.start()

# Allow pipeline to process data + termination
    time.sleep(2.0)

# 🔑 FORCE CLEAN SHUTDOWN (control-level termination)
    exec_pipe.stop()

    print("✅ ModelTaskPipeline stopped cleanly after termination signal")

    return exec_pipe



