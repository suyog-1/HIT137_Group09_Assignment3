# This file adds logging and error handling

from tkinter import messagebox  # For showing errors in the GUI displayed in a msg box

def log_action(func):  # Decorator to log when a function is called
    def wrapper(*args, **kwargs):  # Inner wrapper function that intercepts the call
        print(f"Running: {func.__name__}")  # Log the function name to console
        return func(*args, **kwargs)  # Call the original function with its arguments
    return wrapper  # Return the wrapped function to replace the original

def handle_errors(func):  # Decorator to catch and display runtime errors
    def wrapper(*args, **kwargs):  # Inner wrapper function
        try:
            return func(*args, **kwargs)  # Try running the original function
        except Exception as e:  # Catch any exception that occurs
            messagebox.showerror("Error", str(e))  # Show error message in a popup
    return wrapper  # Return the wrapped function to replace the original                        