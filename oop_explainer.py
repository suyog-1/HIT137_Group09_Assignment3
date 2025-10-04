# oop_explainer.py
# This file provides explanations of OOP concepts and AI model metadata
# to be displayed in the Tkinter GUI.

def get_oop_explanation():
    """
    Returns a formatted string explaining OOP concepts demonstrated in the GUI.
    Used in the bottom section of the GUI to educate the user.
    """
    return (
        "• Multiple Inheritance: GUI inherits from Tkinter and ModelRunner\n"
        "• Encapsulation: GUI components wrapped in methods to hide complexity\n"
        "• Polymorphism: ModelRunner methods used for different model types\n"
        "• Image to Text (Salesforce/BLIP AI Model) & Text to Audio (Suno/Bark AI Model)\n"
        "• Method Overriding: e.g., display_output could be overridden in subclasses\n"
        "• Multiple Decorators: Logging and error handling via @log_action and @handle_errors"
    )

def get_blip_info():
    """
    Returns formatted information about the BLIP (Bootstrapping Language-Image Pre-training) model.
    This is displayed in the GUI when the Image-to-Text model is selected.
    """
    return get_model_info(
        "Salesforce/blip-image-captioning-base",  # Model name
        "Vision-Language",  # Model category
        "BLIP generates natural language descriptions from images using transformer architecture."  # Short description
    )

def get_bark_info():
    """
    Returns formatted information about the Bark text-to-speech model.
    This is displayed in the GUI when the Text-to-Speech model is selected.
    """
    return get_model_info(
        "suno/bark",  # Model name
        "Audio Generation",  # Model category
        "Bark is a transformer-based text-to-speech model that generates highly realistic, multilingual speech with music, background noise, and emotional tone."  # Short description
    )

def get_model_info(name, category, description):
    """
    Helper function to format model information consistently for display in the GUI.
    Accepts model name, category, and a short description, returns a formatted string.
    """
    return f"Model Name: {name}\nCategory: {category}\nShort Description: {description}"
