# Prediction interface for Cog ⚙️
# For more information, see: https://github.com/replicate/cog/blob/main/docs/python.md
import uuid

# Import necessary classes from the cog library for creating a predictor interface.
from cog import BasePredictor, Input
from cog import Path as CogPath
import sys
import time
import torch
# Import custom modules for global settings and model management.
import core.globals
import core.model_manager
# Import the pre-configured face enhancer and face swapping modules.
from core.face_enhancer import face_enhancer
from core.face_swap_picture import faceSwapPicture

# Check if a CUDA-enabled GPU is available.
if not torch.cuda.is_available():
    # If not, set the execution provider to CPU for ONNX Runtime.
    core.globals.providers = ['CPUExecutionProvider']
    print("No GPU detected. Using CPU instead.")

import os
# Import OpenCV for image processing.
import cv2
# Import Iterator for type hinting the return value of the predict method.
from typing import Iterator
# Import subprocess functions to run shell commands.
from subprocess import call, check_call

# Import utility functions for image checks and modifications.
from core.utils import add_white_side
# Import a utility function to detect faces in an image.
from core.config import get_face


def status(string):
    """Prints a status message to the console."""
    print("Status: " + string)


def run_cmd(command):
    """Executes a shell command."""
    try:
        call(command, shell=True)
    except KeyboardInterrupt:
        print("Process interrupted")
        sys.exit(1)


class Predictor(BasePredictor):
    """
    A predictor class that defines the model's setup and prediction logic.
    Inherits from cog.BasePredictor.
    """
    def setup(self):
        """
        Initial setup method. This runs once when the model is loaded into memory.
        """
        # A delay to allow system resources to stabilize.
        time.sleep(10)
        # Run nvidia-smi to verify GPU status.
        check_call("nvidia-smi", shell=True)
        # Assert that a CUDA-enabled GPU is available, otherwise the program will stop.
        assert torch.cuda.is_available()

    def predict(
            self,
            source: CogPath = Input(description="Source image with the face to be used."),
            target: CogPath = Input(description="Target image where the face will be swapped."),
            is_enhancer: bool = Input(description="Enable face enhancement on the result.", default=False),
            keep_fps: bool = Input(description="Keep FPS (not used in this image-to-image context).", default=True),
            keep_frames: bool = Input(description="Keep Frames (not used in this image-to-image context).", default=True),
    ) -> Iterator[CogPath]:
        """
        The main prediction method. This runs every time a new prediction is requested.
        """
        # Print the input paths and options for debugging purposes.
        print("source: ", source)
        print("target: ", target)
        print("keep_fps: ", keep_fps)
        print("keep_frames: ", keep_frames)

        # Convert the CogPath objects to standard string paths.
        source = str(source)
        target = str(target)

        # Add a white border to the source image to help with face detection at the edges.
        source = add_white_side(source)

        # --- Validation Step ---
        # Read the source image and check if a face is present.
        source_face = get_face(cv2.imread(source))
        if not source_face:
            print("\n[WARNING] No face detected in source image. Please try with another one.\n")
            return

        # Read the target image and check if a face is present.
        target_face = get_face(cv2.imread(target))
        if not target_face:
            print("\n[WARNING] No face detected in target image. Please try with another one.\n")
            return

        # --- Face Swapping Step ---
        # Perform the face swap from the source image to the target image.
        output = faceSwapPicture.swap(source=source, target=target)

        # Conditionally enhance the face in the output image if the option is enabled.
        if is_enhancer:
            result = face_enhancer.enhancer_image(target_path=output, output_path=output)

        # Yield the path to the final output image.
        yield CogPath(output)
        # Print a final status message.
        status("img swap successful!")
        return