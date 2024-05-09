import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from ttkbootstrap import Style
import subprocess

from login import LoginWindow


def switch_to_main():
    # Forget all widgets in the root window
    for widget in root.winfo_children():
        widget.pack_forget()

    # Function to handle the successful login event
    def on_login_success(user_id, user_name):
        global user_id_value
        user_id_value = user_id
        user_id_label.config(text=f"Welcome {user_name}, User ID: {user_id}")
        # Hide login and register buttons, show logout button
        login_button.pack_forget()
        register_button.pack_forget()
        logout_button.pack(anchor='nw', padx=20, pady=10)

    # Function to handle the logout event
    def logout():
        global user_id_value
        user_id_value = 0
        user_id_label.config(text=" Welcome Guest, Please sign up or login :")
        # Forget all buttons and re-add them in the original order
        for button in [login_button, register_button, upload_button, real_time_button, analysis_button, logout_button]:
            button.pack_forget()
        login_button.pack(pady=15)
        register_button.pack(pady=15)
        upload_button.pack(pady=15)
        real_time_button.pack(pady=15)
        analysis_button.pack(pady=15)

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

    # Initialize user_id_value to 0
    global user_id_value
    user_id_value = 0

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

    # Create a placeholder for the user_id_label
    user_id_label = tk.Label(right_frame, text=" Welcome Guest, Please sign up or login :", font=("Helvetica", 12))
    user_id_label.pack(anchor='nw', padx=20, pady=10)

    login_button = tk.Button(right_frame, text="Login", command=login, **button_style)
    register_button = tk.Button(right_frame, text="Register", command=register, **button_style)
    logout_button = tk.Button(right_frame, text="Logout", command=logout, **button_style)

    upload_button = tk.Button(right_frame, text="Upload Image", command=upload_image, **button_style)
    real_time_button = tk.Button(right_frame, text="Real-time Analysis", command=real_time_analysis, **button_style)
    analysis_button = tk.Button(right_frame, text="Analysis", command=analysis, **button_style)

    login_button.pack(pady=15)
    register_button.pack(pady=15)
    upload_button.pack(pady=15)
    real_time_button.pack(pady=15)
    analysis_button.pack(pady=15)


# Function to handle the successful login event
def on_login_success(user_id, user_name):
    global user_id_value
    user_id_value = user_id
    user_id_label.config(text=f"Welcome {user_name}, User ID: {user_id}")
    # Hide login and register buttons, show logout button
    login_button.pack_forget()
    register_button.pack_forget()
    logout_button.pack(anchor='nw', padx=20, pady=10)


# Function to handle the logout event
def logout():
    global user_id_value
    user_id_value = 0
    user_id_label.config(text=" Welcome Guest, Please sign up or login :")
    # Forget all buttons and re-add them in the original order
    for button in [login_button, register_button, upload_button, real_time_button, analysis_button, logout_button]:
        button.pack_forget()
    login_button.pack(pady=15)
    register_button.pack(pady=15)
    upload_button.pack(pady=15)
    real_time_button.pack(pady=15)
    analysis_button.pack(pady=15)


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


def change_description(direction):
    global current_description_index
    if direction == "prev":
        current_description_index = (current_description_index - 1) % len(descriptions)
    elif direction == "next":
        current_description_index = (current_description_index + 1) % len(descriptions)

    if isinstance(descriptions[current_description_index], str):
        description_text.config(state=tk.NORMAL)
        description_text.delete(1.0, tk.END)
        description_text.insert(tk.END, descriptions[current_description_index])
        description_text.config(state=tk.DISABLED)
    elif isinstance(descriptions[current_description_index], Image.Image):
        show_image(descriptions[current_description_index])

    current_content_label.config(text=f"{current_description_index + 1}")


def auto_change_description():
    change_description("next")
    root.after(timer_interval, auto_change_description)


def show_image(image):
    description_text.config(state=tk.NORMAL)
    description_text.delete(1.0, tk.END)

    photo = ImageTk.PhotoImage(image)
    description_text.image_create(tk.END, image=photo)

    description_text.config(state=tk.DISABLED)
    description_text.photo = photo


# Initialize user_id_value to 0
global user_id_value
user_id_value = 0

# Create the main window with ttkbootstrap style
style = Style(theme="flatly")  # You can choose a different theme

# Configure main window dimensions
window_width = 850
window_height = 650
root = style.master
root.title("Stress Analysis Application")
root.geometry(f"{window_width}x{window_height}")

# Get started page widgets
background_image = Image.open("img/white.jpg")
background_image = background_image.resize((850, 650))
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.pack()

main_frame = tk.Frame(root, bg="white", width=600, height=400, bd=1, relief=tk.SOLID)
main_frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

info_label = tk.Label(main_frame, text="Welcome to Facial Stress Analysis System", font=("Helvetica", 18),
                      bg="white")
info_label.pack(pady=(20, 25))

content_frame = tk.Frame(main_frame, bg="white", width=600, height=500)
content_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

description_text = tk.Text(content_frame, height=14, width=60, wrap=tk.WORD, font=("Helvetica", 14))
description_text.pack(pady=10)

button_frame = tk.Frame(content_frame, bg="white")
button_frame.pack()

prev_button = ttk.Button(button_frame, text="<", style="Navigation.TButton",
                         command=lambda: change_description("prev"), width=2)
prev_button.pack(side=tk.LEFT, padx=(0, 5))

current_content_label = tk.Label(button_frame, text="1", font=("Helvetica", 10), bg="white")
current_content_label.pack(side=tk.LEFT, padx=(5, 5))

next_button = ttk.Button(button_frame, text=">", style="Navigation.TButton",
                         command=lambda: change_description("next"), width=2)
next_button.pack(side=tk.LEFT, padx=(5, 0))

# Create a frame for the Get Started button
get_started_frame = tk.Frame(content_frame, bg="white")
get_started_frame.pack(pady=(20, 0))

# Create the Get Started button in the new frame
get_started_button = tk.Button(get_started_frame, text="Get Started", command=switch_to_main, width=20, height=1, font=("Helvetica", 16))
get_started_button.pack()


image1 = Image.open("img/start.png")
image1 = image1.resize((650, 350))

image2 = Image.open("img/stresslevel.jpeg")
image2 = image2.resize((650, 350))

image3 = Image.open("img/face.png")
image3 = image3.resize((650, 480))

descriptions = [
    image1,
    image2,
    image3,
    "Welcome to FSIA - the Facial Stress Index Analyzer System.\n\n"
    "FSIA is a cutting-edge tool designed to assess your stress levels through facial image analysis. \n\n"
    "Features:\n"
    "• Accurate stress assessments without specialized equipment\n"
    "• Upload facial images or capture them in real-time\n"
    "• Receive immediate insights into stress patterns\n"
    "• Intuitive interface for a seamless experience\n"
    "• Robust privacy measures to safeguard your data\n\n"
    "Join us on this journey towards a stress-free life with FSIA - where stress assessment meets simplicity.",
]
current_description_index = 0
change_description("next")
change_description("next")
change_description("next")
timer_interval = 5000
root.after(0, auto_change_description)

# Create and configure a frame on the right side for buttons and selections
right_frame = tk.Frame(root)
style.configure("TFrame", background="#4a90e2")  # Set background color for the right frame
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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

# Create a placeholder for the user_id_label
user_id_label = tk.Label(right_frame, text=" Welcome Guest, Please sign up or login :", font=("Helvetica", 12))

login_button = tk.Button(right_frame, text="Login", command=login, **button_style)
register_button = tk.Button(right_frame, text="Register", command=register, **button_style)
logout_button = tk.Button(right_frame, text="Logout", command=logout, **button_style)

upload_button = tk.Button(right_frame, text="Upload Image", command=upload_image, **button_style)
real_time_button = tk.Button(right_frame, text="Real-time Analysis", command=real_time_analysis, **button_style)
analysis_button = tk.Button(right_frame, text="Analysis", command=analysis, **button_style)


root.mainloop()
