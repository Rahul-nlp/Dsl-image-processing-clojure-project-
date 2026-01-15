from model.image_job import ImageJob

# File 7: Termination signal
termination_signal = ImageJob(
    image_id="TERMINATE_SIGNAL",
    is_termination=True,
    is_poison_pill=True,
    transformations=["control_signal"]
)