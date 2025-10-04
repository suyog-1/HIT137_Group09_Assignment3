import tkinter as tk  # Core GUI toolkit for building desktop applications
from tkinter import filedialog, messagebox, ttk  # Additional widgets and dialogs for user interaction
from PIL import Image  # Used to load and process image files for captioning
from decorators import log_action, handle_errors  # Custom decorators for logging and error handling
from model_runner import ModelRunner  # Class that runs AI models (BLIP and Bark)
from oop_explainer import get_oop_explanation, get_model_info  # Functions to display OOP concepts and model metadata

class AIModelGUI(tk.Tk, ModelRunner):  # Inherits from Tkinter's main window and model logic class
    def __init__(self):  # Constructor method to initialize the GUI
        super().__init__()  # Calls parent constructors (Tk and ModelRunner)
        self.title("HIT137 AI Model Display")  # Sets the window title
        self.geometry("800x700")  # Defines the window size in pixels
        self.configure(bg="#f0f0f0")  # Sets a light gray background color

        self.input_type = tk.StringVar(value="Text")  # Tracks whether user selects Text or Image input
        self.file_path = None  # Stores the path of the selected image file
        self.text_input_box = None  # Will hold the text input widget for TTS
        self.caption_output_box = None  # Will hold the output widget for image captions
        self.model_info = None  # Will hold the label displaying model metadata

        self.create_widgets()  # Builds all GUI components by calling setup methods

    def create_widgets(self):  # Organizes GUI component creation into modular methods
        self.create_model_selection()  # Adds dropdown for selecting model type
        self.create_input_section()  # Adds radio buttons and file browser
        self.create_buttons()  # Adds Run and Clear buttons
        self.create_output_section()  # Adds input/output boxes for TTS and captioning
        self.create_model_info()  # Adds section to display model metadata
        self.create_oop_explanation()  # Adds static explanation of OOP concepts

    def create_model_selection(self):  # Creates dropdown for selecting AI model
        ttk.Label(self, text="AI Model Selection", font=("Arial",15)).pack(pady=20)  # Adds label above dropdown
        self.model_dropdown = ttk.Combobox(self, values=["Image-to-Text", "Text-to-Speech"])  # Dropdown with model options
        self.model_dropdown.set("Image-to-Text")  # Sets default selection to image captioning
        self.model_dropdown.pack()  # Adds dropdown to the GUI layout

    def create_input_section(self):  # Creates section for selecting input type
        frame = tk.Frame(self)  # Creates a container frame for layout
        frame.pack(pady=10)  # Adds vertical spacing below the frame
        ttk.Label(frame, text="User Input Section", font=("Arial",10)).grid(row=0, column=0)  # Adds label inside the frame
        ttk.Radiobutton(frame, text="Text", variable=self.input_type, value="Text").grid(row=1, column=0)  # Radio button for text input
        ttk.Radiobutton(frame, text="Image", variable=self.input_type, value="Image").grid(row=1, column=1)  # Radio button for image input
        ttk.Button(frame, text="Browse", command=self.browse_file).grid(row=1, column=2)  # Button to open file dialog

    def create_buttons(self):  # Adds buttons to run models and clear output
        frame = tk.Frame(self)  # Creates a container frame
        frame.pack(pady=10)  # Adds spacing below the frame
        ttk.Button(frame, text="Run Image-to-Text Model", command=self.run_model_1).grid(row=0, column=0)  # Button to run BLIP
        ttk.Button(frame, text="Run Text-to-Speech Model", command=self.run_model_2).grid(row=0, column=1)  # Button to run Bark
        ttk.Button(frame, text="Clear", command=self.clear_output).grid(row=0, column=2)  # Button to clear output and reset

    def create_output_section(self):  # Creates separate input/output boxes for TTS and captioning
        ttk.Label(self, text="Text Input (for TTS)", font=("Arial",10)).pack(pady=10)  # Label for TTS input box
        self.text_input_box = tk.Text(self, height=5, width=80)  # Editable text box for user input
        self.text_input_box.pack()  # Adds text input box to GUI

        ttk.Label(self, text="Image Caption Output", font=("Arial",10)).pack(pady=10)  # Label for caption output box
        self.caption_output_box = tk.Text(self, height=5, width=80, state="disabled")  # Read-only box for displaying captions
        self.caption_output_box.pack()  # Adds caption output box to GUI

        self.update_input_visibility()  # Sets initial visibility based on selected input type
        self.input_type.trace_add("write", lambda *args: self.update_input_visibility())  # Updates visibility when input type changes

    def update_input_visibility(self):  # Dynamically toggles visibility of input/output boxes
        if self.input_type.get() == "Text":  # If user selects Text input
            self.text_input_box.config(state="normal")  # Enable text input box
            self.caption_output_box.config(state="disabled")  # Disable caption output box
        else:  # If user selects Image input
            self.text_input_box.config(state="disabled")  # Disable text input box
            self.caption_output_box.config(state="normal")  # Enable caption output box

    def create_model_info(self):  # Adds section to display model metadata
        ttk.Label(self, text="Model Information & Explanation", font=("Arial",10)).pack(pady=10)  # Label for model info section
        self.model_info = tk.Label(self, text="Run a Model to see it's information", justify="left", bg="#f0f0f0")  # Label to show model name, category, and description
        self.model_info.pack()  # Adds model info label to GUI

    def create_oop_explanation(self):  # Adds static explanation of OOP concepts
        ttk.Label(self, text="OOP Concept Explanations:", font=("Arial",10)).pack(pady=10)  # Label for OOP section
        explanation = get_oop_explanation()  # Retrieves formatted explanation string
        tk.Label(self, text=explanation, justify="left", bg="#f0f0f0").pack()  # Displays explanation in a label

    def browse_file(self):  # Opens file dialog to select an image
        self.file_path = filedialog.askopenfilename()  # Stores selected file path for captioning

    @log_action  # Logs method call to console
    @handle_errors  # Catches and displays errors in a messagebox
    def run_model_1(self):  # Runs BLIP image captioning model
        if self.input_type.get() == "Image" and self.file_path:  # Checks if input type is Image and file is selected
            caption = self.run_image_captioning(self.file_path)  # Runs BLIP model and gets caption
            self.caption_output_box.config(state="normal")  # Enables caption box for writing
            self.caption_output_box.delete("1.0", tk.END)  # Clears previous output
            self.caption_output_box.insert(tk.END, f"Caption: {caption}\n")  # Inserts new caption
            self.caption_output_box.config(state="disabled")  # Locks caption box to prevent editing
            info = get_model_info("Salesforce/blip-image-captioning-base", "Vision", "BLIP image captioning model.")  # Gets model metadata
            self.model_info.config(text=info)  # Displays model info
        else:
            messagebox.showinfo("More information needed", "Please select an image file.")  # Prompts user to select image

    @log_action  # Logs method call to console
    @handle_errors  # Catches and displays errors in a messagebox
    def run_model_2(self):  # Runs Bark text-to-speech model
        if self.input_type.get() == "Text":  # Checks if input type is Text
            text = self.text_input_box.get("1.0", tk.END).strip()  # Retrieves and trims user input
            if text:  # Checks if input is not empty
                self.run_text_to_speech(text)  # Runs Bark model and plays audio
                info = get_model_info("suno/bark", "Audio", "Neural text-to-speech model.")  # Gets model metadata
                self.model_info.config(text=info)  # Displays model info
            else:
                messagebox.showinfo("More information needed", "Please enter text to speak.")  # Prompts user to enter text
        else:
            messagebox.showinfo("More information needed", "Text input required for TTS.")  # Warns user if wrong input type

    def clear_output(self):  # Clears all user input and output
        self.text_input_box.delete("1.0", tk.END)  # Clears text input box
        self.caption_output_box.config(state="normal")  # Enables caption box for clearing



