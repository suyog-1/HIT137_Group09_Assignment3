# model_runner.py — Handles AI model logic using Hugging Face and subprocess for audio playback

from PIL import Image  # Imports Python Imaging Library to load and process image files
from transformers import pipeline  # Imports Hugging Face's pipeline API for easy model access
import scipy.io.wavfile  # Provides functions to write audio data to WAV format
import tempfile  # Allows creation of temporary files for storing audio output
import subprocess  # Enables launching external applications like media players
import numpy as np  # Imports NumPy for handling audio arrays and tensor operations

class ModelRunner:  # Defines a reusable class to encapsulate AI model logic
    def run_image_captioning(self, image_path):  # Method to generate captions from images using BLIP
        image = Image.open(image_path)  # Opens the image file using PIL
        pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")  # Loads BLIP model via Hugging Face pipeline
        result = pipe(image)  # Runs inference on the image to generate a caption
        return result[0]['generated_text']  # Extracts and returns the generated caption text

    def run_text_to_speech(self, text):  # Method to convert input text into speech using Bark
        pipe = pipeline("text-to-audio", model="suno/bark")  # Load Bark model via Hugging Face pipeline

        result = pipe(text)  # Run inference on the input text to generate audio output

        # Validate that the result is a dictionary with expected keys
        if isinstance(result, dict) and "audio" in result and "sampling_rate" in result:
            audio_array = result["audio"]  # Extract the audio waveform as a NumPy array
            sample_rate = result["sampling_rate"]  # Extract the sample rate (e.g., 24000 Hz)
        else:
            raise TypeError(f"Unexpected output format from Bark: {result}")  # Raise error if format is invalid

        # Bark returns audio in shape (1, N) — flatten to 1D for WAV compatibility
        if isinstance(audio_array, np.ndarray) and audio_array.ndim == 2:  # Check if audio is a 2D array
            audio_array = audio_array.squeeze()  # Convert shape from (1, N) to (N,) for proper WAV formatting

        # Create a temporary WAV file to store the audio output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:  # Create a temp file with .wav extension
            tmp_path = tmp.name  # Save the file path before closing the file
            scipy.io.wavfile.write(tmp_path, rate=sample_rate, data=audio_array)  # Write audio data to the WAV file

        # Play the audio file using the system's default media player (Windows only)
        subprocess.run(["start", "", tmp_path], shell=True)  # Launch the file using 'start' to open with default app



