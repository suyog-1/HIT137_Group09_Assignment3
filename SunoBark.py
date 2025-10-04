# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("text-to-speech", model="suno/bark")