import tkinter as tk  # Core GUI toolkit for building desktop applications
from tkinter import filedialog, messagebox, ttk  # Additional widgets and dialogs for user interaction
from PIL import Image, ImageTk  # Used to load and process image files for captioning and display
from decorators import log_action, handle_errors  # Custom decorators for logging and error handling
from model_runner import ModelRunner  # Class that runs AI models (BLIP and Bark)
from oop_explainer import get_oop_explanation, get_blip_info, get_bark_info  # Functions to display OOP concepts and model metadata

class AIModelGUI(tk.Tk, ModelRunner):  # Inherits from Tkinter's main window and model logic class
    def __init__(self):  # Constructor method to initialize the GUI
        super().__init__()  # Calls parent constructors (Tk and ModelRunner)
        self.state('zoomed')  # Opens window in maximized mode to ensure all content is visible
        self.title("HIT137 AI Model Display")  # Sets the window title
        self.geometry("800x700")  # Defines the default window size in pixels (used when not maximized)
        self.configure(bg="#f0f0f0")  # Sets a light gray background color

        self.selected_model = tk.StringVar(value="Image-to-Text")  # Tracks which AI model is selected from dropdown
        self.file_path = None  # Stores the path of the selected image file
        self.text_input_box = None  # Will hold the text input widget for TTS
        self.caption_output_box = None  # Will hold the output widget for image captions
        self.model_info = None  # Will hold the text widget displaying model metadata
        self.status_label = None  # Will hold the status bar label for showing operation progress
        self.selected_file_frame = None  # Will hold the frame for displaying selected file info
        self.selected_file_label = None  # Will hold the label showing selected filename
        self.file_browse_button = None  # Will hold the browse button for image selection
        self.text_input_label = None  # Will hold the label for text input section

        self.create_widgets()  # Builds all GUI components by calling setup methods

    def create_widgets(self):  # Organizes GUI component creation into modular methods
        self.create_model_selection()  # Adds dropdown for selecting AI model type
        self.create_input_section()  # Adds input areas for both text and image
        self.create_buttons()  # Adds Run and Clear buttons
        self.create_output_section()  # Adds output box for image captions
        self.create_model_info()  # Adds section to display model metadata
        self.create_oop_explanation()  # Adds static explanation of OOP concepts
        self.create_status_bar()  # Adds status bar at bottom for operation feedback
        self.update_ui_states()  # Sets initial UI state based on default model selection

    def create_model_selection(self):  # Creates dropdown for selecting AI model
        ttk.Label(self, text="AI Model Selection", font=("Arial", 15)).pack(pady=20)  # Adds label above dropdown
        self.model_dropdown = ttk.Combobox(self, textvariable=self.selected_model, 
                                         values=["Image-to-Text", "Text-to-Speech"], 
                                         state="readonly")  # Dropdown with model options, readonly to prevent typing
        self.model_dropdown.pack()  # Adds dropdown to the GUI layout
        self.selected_model.trace_add("write", lambda *args: self.update_ui_states())  # Updates UI when selection changes

    def create_input_section(self):  # Creates section for user input based on model type
        # Main input frame to contain all input elements
        input_main_frame = ttk.Frame(self)
        input_main_frame.pack(pady=10, fill="x", padx=20)  # Adds spacing and makes frame expand horizontally
        
        ttk.Label(input_main_frame, text="User Input Section", font=("Arial", 12)).pack(anchor="w", pady=(0, 10))  # Section title

        # Text input area (for Text-to-Speech) - contained in labeled frame for better organization
        text_frame = ttk.LabelFrame(input_main_frame, text="Text Input (for Text-to-Speech)")
        text_frame.pack(fill="x", pady=5)  # Makes frame expand horizontally with vertical spacing
        
        self.text_input_box = tk.Text(text_frame, height=4, width=80)  # Editable text box for user input
        self.text_input_box.pack(fill="x", padx=5, pady=5)  # Adds text input box to GUI with padding

        # File input area (for Image-to-Text) - contained in labeled frame for better organization
        file_frame = ttk.LabelFrame(input_main_frame, text="Image Input (for Image-to-Text)")
        file_frame.pack(fill="x", pady=5)  # Makes frame expand horizontally with vertical spacing
        
        # Browse button and file display in same row for compact layout
        browse_frame = ttk.Frame(file_frame)
        browse_frame.pack(fill="x", padx=5, pady=5)  # Creates frame for browse elements
        
        self.file_browse_button = ttk.Button(browse_frame, text="Browse Image", command=self.browse_file)
        self.file_browse_button.pack(side="left", padx=(0, 10))  # Positions browse button on left with spacing
        
        # Selected file display area with clear button
        self.selected_file_frame = ttk.Frame(browse_frame)
        self.selected_file_frame.pack(side="left", fill="x", expand=True)  # Makes file display expand to fill space
        
        self.selected_file_label = ttk.Label(self.selected_file_frame, text="No file selected", 
                                           background="#f5f5f5", relief="solid", padding=5)  # Label to show selected filename
        self.selected_file_label.pack(side="left", fill="x", expand=True)  # Positions label to expand horizontally
        
        self.clear_file_btn = ttk.Button(self.selected_file_frame, text="✕", width=3, 
                                       command=self.clear_selected_file)  # Button to clear file selection
        self.clear_file_btn.pack(side="right")  # Positions clear button on right side

    def create_buttons(self):  # Adds buttons to run model and clear output
        frame = ttk.Frame(self)  # Creates a container frame
        frame.pack(pady=15)  # Adds spacing below the frame
        self.run_model_button = ttk.Button(frame, text="Run Model", command=self.run_current_model)  # Single button for both models
        self.run_model_button.pack(side="left", padx=5)  # Positions run button with spacing
        ttk.Button(frame, text="Clear All", command=self.clear_output).pack(side="left", padx=5)  # Button to clear all inputs and outputs

    def create_output_section(self):  # Creates output box for image captions
        output_frame = ttk.Frame(self)  # Creates container frame for output section
        output_frame.pack(fill="x", pady=10, padx=20)  # Makes frame expand horizontally with spacing
        
        ttk.Label(output_frame, text="Image Caption Output", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))  # Label for output box
        self.caption_output_box = tk.Text(output_frame, height=5, width=80)  # Text box for displaying image captions
        self.caption_output_box.pack(fill="x")  # Adds caption output box to GUI

    def create_model_info(self):  # Adds section to display model metadata
        info_frame = ttk.Frame(self)  # Creates container frame for model info
        info_frame.pack(fill="x", pady=10, padx=20)  # Makes frame expand horizontally with spacing
        
        ttk.Label(info_frame, text="Model Information & Explanation", font=("Arial", 12)).pack(anchor="w")  # Label for model info section
        self.model_info = tk.Text(info_frame, height=6, width=80, wrap="word", 
                                bg="#f0f0f0", relief="flat", font=("Arial", 9))  # Text widget for model info with custom styling
        self.model_info.pack(fill="x", pady=5)  # Adds model info widget to GUI
        self.model_info.insert("1.0", "Select a model to see its information and explanation.")  # Default placeholder text
        self.model_info.config(state="disabled")  # Makes model info read-only

    def create_oop_explanation(self):  # Adds static explanation of OOP concepts
        explanation_frame = ttk.Frame(self)  # Creates container frame for OOP explanation
        explanation_frame.pack(fill="x", pady=10, padx=20)  # Makes frame expand horizontally with spacing
        
        ttk.Label(explanation_frame, text="OOP Concept Explanations:", font=("Arial", 12)).pack(anchor="w")  # Label for OOP section
        explanation_text = tk.Text(explanation_frame, height=8, width=80, wrap="word", 
                                 bg="#f0f0f0", relief="flat", font=("Arial", 9))  # Text widget for OOP explanation
        explanation_text.pack(fill="x", pady=5)  # Adds explanation widget to GUI
        explanation_text.insert("1.0", get_oop_explanation())  # Inserts OOP explanation text
        explanation_text.config(state="disabled")  # Makes explanation read-only

    def create_status_bar(self):  # Creates status bar at bottom of window for operation feedback
        status_frame = ttk.Frame(self, height=28, relief="sunken")  # Creates status bar frame with fixed height and border
        status_frame.pack(fill="x", side="bottom")  # Positions status bar at bottom and makes it expand horizontally
        status_frame.pack_propagate(False)  # Prevents frame from shrinking based on content
        
        self.status_label = ttk.Label(status_frame, text="Ready", background="#e0e0e0")  # Label for status messages
        self.status_label.pack(side="left", padx=10)  # Positions status label with padding

    def update_ui_states(self):  # Updates UI element states based on selected model without removing any elements
        """Update UI element states based on selected model without removing anything"""
        model = self.selected_model.get()  # Gets currently selected model from dropdown
        
        if model == "Image-to-Text":  # If Image-to-Text model is selected
            # Enable image-related elements, disable text input with visual indication
            self.text_input_box.config(state="disabled", bg="#f5f5f5")  # Gray out text input area
            self.file_browse_button.config(state="normal")  # Enable file browse button
            self.caption_output_box.config(state="normal", bg="white")  # Enable caption output area
            # Update model info display with BLIP model information
            info = get_blip_info()  # Gets BLIP model info from oop_explainer
            self.update_model_info_display(info)  # Updates model info display
            
        else:  # If Text-to-Speech model is selected
            # Enable text input, disable image-related elements with visual indication
            self.text_input_box.config(state="normal", bg="white")  # Enable text input area
            self.file_browse_button.config(state="disabled")  # Disable file browse button
            self.caption_output_box.config(state="disabled", bg="#f5f5f5")  # Gray out caption output area
            # Update model info display with Bark model information
            info = get_bark_info()  # Gets Bark model info from oop_explainer
            self.update_model_info_display(info)  # Updates model info display
        
        self.update_idletasks()  # Forces UI update to ensure changes are visible immediately

    def update_model_info_display(self, info_text):  # Updates the model info display with formatted text
        """Update the model info display with formatted text"""
        self.model_info.config(state="normal")  # Temporarily enable text widget for editing
        self.model_info.delete("1.0", tk.END)  # Clear existing content
        self.model_info.insert("1.0", info_text)  # Insert new model information
        self.model_info.config(state="disabled")  # Make text widget read-only again

    def browse_file(self):  # Opens file dialog to select an image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]  # Filters for image files only
        )
        if file_path:  # If user selected a file (didn't cancel dialog)
            self.file_path = file_path  # Stores selected file path for captioning
            file_name = file_path.split("/")[-1]  # Extracts just the filename from the full path
            self.selected_file_label.config(text=f"Selected: {file_name}")  # Updates label with filename
            self.update_status(f"Selected file: {file_name}")  # Updates status bar

    def clear_selected_file(self):  # Clears the currently selected file
        self.file_path = None  # Clears stored file path
        self.selected_file_label.config(text="No file selected")  # Resets file display label
        self.update_status("File selection cleared")  # Updates status bar

    def update_status(self, message):  # Updates the status bar with a message
        if self.status_label:  # Checks if status label exists
            self.status_label.config(text=message)  # Updates status label text
        self.update_idletasks()  # Forces UI update to ensure status change is visible immediately

    @log_action  # Logs method call to console
    @handle_errors  # Catches and displays errors in a messagebox
    def run_current_model(self):  # Runs the currently selected AI model based on dropdown selection
        model = self.selected_model.get()  # Gets currently selected model from dropdown
        self.update_status(f"Running {model} model...")  # Updates status bar to show operation in progress

        if model == "Image-to-Text":  # If Image-to-Text model is selected
            if self.file_path:  # Checks if an image file is selected
                try:
                    caption = self.run_image_captioning(self.file_path)  # Runs BLIP model and gets caption
                    self.caption_output_box.config(state="normal")  # Enables caption box for writing
                    self.caption_output_box.delete("1.0", tk.END)  # Clears previous output
                    self.caption_output_box.insert(tk.END, f"Caption: {caption}\n")  # Inserts new caption
                    self.update_status(f"{model} completed!")  # Updates status bar on completion
                except Exception as e:
                    self.update_status(f"Error: {str(e)}")  # Updates status bar with error message
                    raise  # Re-raises exception for error handling decorator
            else:
                messagebox.showinfo("More information needed", "Please select an image file.")  # Prompts user to select image
        else:  # If Text-to-Speech model is selected
            text = self.text_input_box.get("1.0", tk.END).strip()  # Retrieves and trims user input from text box
            if text:  # Checks if input is not empty
                try:
                    self.run_text_to_speech(text)  # Runs Bark model and plays audio
                    self.update_status(f"{model} completed!")  # Updates status bar on completion
                except Exception as e:
                    self.update_status(f"Error: {str(e)}")  # Updates status bar with error message
                    raise  # Re-raises exception for error handling decorator
            else:
                messagebox.showinfo("More information needed", "Please enter text to speak.")  # Prompts user to enter text

    def clear_output(self):  # Clears all user input and output
        # Clear text input area
        self.text_input_box.config(state="normal")  # Ensures text input is editable
        self.text_input_box.delete("1.0", tk.END)  # Clears text input box
        
        # Clear caption output area
        self.caption_output_box.config(state="normal")  # Ensures caption output is editable
        self.caption_output_box.delete("1.0", tk.END)  # Clears caption output box
        
        # Clear file selection
        self.clear_selected_file()  # Calls method to clear file selection
        
        # Reset UI states based on current model selection
        self.update_ui_states()  # Ensures UI reflects cleared state properly
        
        self.update_status("All outputs cleared")  # Updates status bar