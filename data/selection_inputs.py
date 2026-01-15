from model.image_job import ImageJob

# File 6: 3 variants of same image for selection node (1-of-n)
selection_variants = [
    # Method A: Gaussian denoise
    ImageJob(
        image_id="night_photo_gaussian",
        transformations=["loaded", "gaussian_denoise"],
        current_format="JPG",
        quality_score=0.82,
        correlation_id="night_photo_001",  # Same correlation for all variants
        processed_by=["gaussian_processor"]
    ),
    # Method B: Median denoise
    ImageJob(
        image_id="night_photo_median",
        transformations=["loaded", "median_denoise"],
        current_format="JPG",
        quality_score=0.95,
        correlation_id="night_photo_001",  # Same correlation
        processed_by=["median_processor"]
    ),
    # Method C: Bilateral denoise
    ImageJob(
        image_id="night_photo_bilateral",
        transformations=["loaded", "bilateral_denoise"],
        current_format="JPG",
        quality_score=0.93,
        correlation_id="night_photo_001",  # Same correlation
        processed_by=["bilateral_processor"]
    )
]