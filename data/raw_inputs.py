from model.image_job import ImageJob

# File 1: Basic images starting the pipeline
raw_images = [
    ImageJob(
        image_id="photo_001",
        transformations=["loaded"],
        current_format="PNG",
        quality_score=0.8
    ),
    ImageJob(
        image_id="photo_002",
        transformations=["loaded"],
        current_format="JPG",
        quality_score=0.7
    ),
    ImageJob(
        image_id="photo_003",
        transformations=["loaded"],
        current_format="RAW",
        quality_score=0.9
    ),
    ImageJob(
        image_id="numeric_001",
        transformations=["loaded"],
        numeric_value=10.5,  # For summator example
        current_format="PNG"
    ),
    ImageJob(
        image_id="numeric_002",
        transformations=["loaded"],
        numeric_value=20.3,  # For summator example
        current_format="PNG"
    ),
        ImageJob(
        image_id="numeric_003",
        transformations=["loaded"],
        numeric_value=10.5,  # For summator example
        current_format="PNG"
    )
]