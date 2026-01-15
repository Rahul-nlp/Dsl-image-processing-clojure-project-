# Data package - your 7 input files
from .raw_inputs import raw_images
from .blur_input import blur_input
from .convert_input import convert_input
from .panorama_inputs import panorama_parts
from .split_input import split_input
from .selection_inputs import selection_variants
from .termination_signal import termination_signal

__all__ = [
    'raw_images',
    'blur_input',
    'convert_input',
    'panorama_parts',
    'split_input',
    'selection_variants',
    'termination_signal'
]