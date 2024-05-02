import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style

from login import LoginWindow


global user_id_value
user_id_value = 0

# Function to handle the successful login event
def on_login_success(user_id):
    global user_id_value
    user_id_value = user_id
    user_id_label.config(text=f"User ID: {user_id}")


# Create the main window with ttkbootstrap style
style = Style(theme="flatly")  # You can choose a different theme

# Configure main window dimensions
window_width = 850
window_height = 650
root = style.master
root.title("Stress Analysis Application")
root.geometry(f"{window_width}x{window_height}")

# Create and configure a main frame with ttkbootstrap style
main_frame = tk.Frame(root)
style.configure("TFrame", background="#4a90e2")  # Set background color for the main frame
main_frame.pack(fill=tk.BOTH, expand=True)

# Load and display an image on the left side
image_path = "img/fsia.png"  # Replace with the path to your image
image = Image.open(image_path)
image = image.resize((450, 500))  # Resize the image without ANTIALIAS
image = ImageTk.PhotoImage(image)

image_label = tk.Label(main_frame, image=image)
image_label.image = image  # Keep a reference to the image
image_label.pack(side=tk.LEFT, padx=20, pady=20)

# Create and configure a frame on the right side for buttons and selections
right_frame = tk.Frame(main_frame)
style.configure("TFrame", background="#4a90e2")  # Set background color for the right frame
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Create and configure labels with more padding and ttkbootstrap style
title_label = tk.Label(right_frame, text="Facial Stress Analysis", font=("Helvetica", 24), pady=20)
style.configure("TLabel", foreground="#ffffff")  # Set text color for labels
title_label.pack()

# Create and configure buttons with enhanced design and ttkbootstrap style
button_style = {
    "font": ("Helvetica", 16),
    "width": 25,
    "height": 2,
    "bg": "#007acc",  # Blue background color
    "fg": "white",  # White text color
    "borderwidth": 2,  # Border width
    "relief": "raised"  # Raised button appearance
}


# Function to handle the login button click
def login():
    try:
        LoginWindow(tk.Toplevel(root), on_login_success)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to handle the register button click
def register():
    try:
        subprocess.Popen(["python", "register.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to handle the upload image button click
def upload_image():
    try:
        # Create an instance of the ImageStressAnalyzer class and run it
        subprocess.Popen(["python", "image_stress_analyzer.py", str(user_id_value)])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Function to handle the real-time analysis button click
def real_time_analysis():
    try:
        # Run the stress.py script using subprocess
        subprocess.Popen(["python", "real_time_analysis.py"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def analysis():
    try:
        # Run the stress.py script using subprocess
        subprocess.Popen(["python", "historical_data_analysis.py", str(user_id_value)])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Create a placeholder for the user_id_label
user_id_label = tk.Label(right_frame, text=" Welcome Guest, Please sign up or login :", font=("Helvetica", 12))
user_id_label.pack(anchor='nw', padx=20, pady=10)

login_button = tk.Button(right_frame, text="Login", command=login, **button_style)
register_button = tk.Button(right_frame, text="Register", command=register, **button_style)
upload_button = tk.Button(right_frame, text="Upload Image", command=upload_image, **button_style)
real_time_button = tk.Button(right_frame, text="Real-time Analysis", command=real_time_analysis, **button_style)
analysis_button = tk.Button(right_frame, text="Analysis", command=analysis, **button_style)

login_button.pack(pady=15)
register_button.pack(pady=15)
upload_button.pack(pady=15)
real_time_button.pack(pady=15)
analysis_button.pack(pady=15)

# Start the main loop
root.mainloop()
