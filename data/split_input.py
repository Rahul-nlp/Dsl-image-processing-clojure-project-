from model.image_job import ImageJob

# File 5: Large image to split (1-to-n)
split_input = ImageJob(
    image_id="large_image",
    transformations=["loaded", "enhanced"],
    current_format="PNG",
    split_into=5,  # Will be split into 4 parts
    quality_score=0.95
)