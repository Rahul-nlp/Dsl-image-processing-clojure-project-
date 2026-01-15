from model.image_job import ImageJob

# File 4: 3 images for panorama stitching (n-to-1)
panorama_parts = [
    ImageJob(
        image_id="panorama_part_001",
        transformations=["loaded"],
        current_format="JPG",
        panorama_group="mountain_view",
        quality_score=0.88
    ),
    ImageJob(
        image_id="panorama_part_002",
        transformations=["loaded"],
        current_format="JPG",
        panorama_group="mountain_view",
        quality_score=0.86
    ),
    ImageJob(
        image_id="panorama_part_003",
        transformations=["loaded"],
        current_format="JPG",
        panorama_group="mountain_view",
        quality_score=0.90
    )
]