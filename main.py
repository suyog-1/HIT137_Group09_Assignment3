# This file launches the Tkinter GUI

from gui_base import AIModelGUI  # Import the main GUI base file

if __name__ == "__main__":  # Runs script directly
    app = AIModelGUI()  # Create an instance of the GUI
    app.mainloop()  # Start the Tkinter loop to keep window open
