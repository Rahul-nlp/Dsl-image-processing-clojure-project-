from model.image_job import ImageJob

# File 3: Input for format conversion node
convert_input = [ ImageJob(
    image_id="photo_001_blurred",
    transformations=["loaded", "color_corrected", "blurred"],
    current_format="PNG",  # Will be converted to JPG
    quality_score=0.82
)
]