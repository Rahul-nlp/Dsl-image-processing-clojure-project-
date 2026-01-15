from model.image_job import ImageJob

# File 2: Inputs for blur node (already partially processed)
blur_input = ImageJob(
    image_id="photo_001_preprocessed",
    transformations=["loaded", "color_corrected"],
    current_format="PNG",
    quality_score=0.85
)