import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from login import LoginWindow

class GetStartPage:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Get Started")
        self.root.geometry("850x650")

        # Load and display the background image
        background_image = Image.open("img/white.jpg")  # Replace with your image file
        background_image = background_image.resize((850, 650))  # Resize the image
        self.background_photo = ImageTk.PhotoImage(background_image)
        background_label = tk.Label(self.root, image=self.background_photo)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a main frame
        main_frame = tk.Frame(self.root, bg="white", width=600, height=400, bd=1, relief=tk.SOLID)
        main_frame.place(relx=0.5, rely=0.45, anchor=tk.CENTER)  # Adjusted rely parameter to position lower

        # Add information labels
        info_label = tk.Label(main_frame, text="Welcome to Facial Stress Analysis System", font=("Helvetica", 18),
                              bg="white")
        info_label.pack(pady=(20, 25))  # Added more padding at the bottom

        # Create a frame for the content and description
        self.content_frame = tk.Frame(main_frame, bg="white", width=600, height=500)  # Resized content frame
        self.content_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Create a text widget for the description
        self.description_text = tk.Text(self.content_frame, height=14, width=60, wrap=tk.WORD, font=("Helvetica", 14))
        self.description_text.pack(pady=10)

        # Add buttons for changing the description content and display current content index
        button_frame = tk.Frame(self.content_frame, bg="white")
        button_frame.pack()

        prev_button = ttk.Button(button_frame, text="<", style="Navigation.TButton",
                                 command=lambda: self.change_description("prev"), width=2)
        prev_button.pack(side=tk.LEFT, padx=(0, 5))

        self.current_content_label = tk.Label(button_frame, text="1", font=("Helvetica", 10), bg="white")
        self.current_content_label.pack(side=tk.LEFT, padx=(5, 5))

        next_button = ttk.Button(button_frame, text=">", style="Navigation.TButton",
                                 command=lambda: self.change_description("next"), width=2)
        next_button.pack(side=tk.LEFT, padx=(5, 0))

        # Load and resize images
        self.image1 = Image.open("img/start.png")  # Replace with your image file
        self.image1 = self.image1.resize((650, 350))  # Resize image to fit content frame

        self.image2 = Image.open("img/stresslevel.jpeg")  # Replace with your image file
        self.image2 = self.image2.resize((650, 350))  # Resize image to fit content frame

        self.image3 = Image.open("img/face.png")  # Replace with your image file
        self.image3 = self.image3.resize((650, 480))  # Resize image to fit content frame

        # Start a timer to automatically change the description
        self.descriptions = [
            self.image1,
            self.image2,
            self.image3,  # Added the new image here
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
        self.current_description_index = 0
        self.change_description("next")  # Initial description
        self.change_description("next")
        self.change_description("next")
        self.timer_interval = 5000  # Time interval in milliseconds (e.g., 5000 ms = 5 seconds)
        self.root.after(0, self.auto_change_description)  # Start immediately

        # Add buttons
        button_container = tk.Frame(main_frame, bg="white")
        button_container.pack(side=tk.BOTTOM, pady=(20, 30))  # Added extra padding below the buttons

        button_padding = 10
        login_button = ttk.Button(button_container, text="Login", style="Main.TButton",
                                  command=self.login_window)
        login_button.pack(side=tk.LEFT, padx=button_padding)

        register_button = ttk.Button(button_container, text="Register", style="Main.TButton",
                                     command=self.open_register_window)
        register_button.pack(side=tk.LEFT, padx=button_padding)

        get_started_button = ttk.Button(button_container, text="Get Started as Guest", style="Main.TButton",
                                        command=self.continue_as_guest)
        get_started_button.pack(side=tk.LEFT, padx=button_padding)

        # Define button styles
        self.style = ttk.Style()
        self.style.configure("Navigation.TButton", font=("Helvetica", 14), background="lightgray", foreground="black")
        self.style.map("Navigation.TButton", background=[("active", "white")])
        self.style.configure("Main.TButton", font=("Helvetica", 14), background="lightblue", foreground="black")
        self.style.map("Main.TButton", background=[("active", "lightcyan")])

    def login_window(self):
        subprocess.Popen(["python", "login.py"])

    def open_register_window(self):
        # Open the register window
        subprocess.Popen(["python", "register.py"])

    def continue_as_guest(self):
        # Continue as guest
        subprocess.Popen(["python", "main.py"])
        self.root.destroy()

    def change_description(self, direction):
        # Update the description text and current content index label
        if direction == "prev":
            self.current_description_index = (self.current_description_index - 1) % len(self.descriptions)
        elif direction == "next":
            self.current_description_index = (self.current_description_index + 1) % len(self.descriptions)

        if isinstance(self.descriptions[self.current_description_index], str):
            self.description_text.config(state=tk.NORMAL)
            self.description_text.delete(1.0, tk.END)
            self.description_text.insert(tk.END, self.descriptions[self.current_description_index])
            self.description_text.config(state=tk.DISABLED)
        elif isinstance(self.descriptions[self.current_description_index], Image.Image):
            self.show_image(self.descriptions[self.current_description_index])

        # Update current content label
        self.current_content_label.config(text=f"{self.current_description_index + 1}")

    def auto_change_description(self):
        # Change the description to the first content (Description 1)
        self.change_description("next")
        # Automatically change the description text from content 1 to content 3
        self.root.after(self.timer_interval, self.auto_change_description)

    def show_image(self, image):
        # Clear existing content
        self.description_text.config(state=tk.NORMAL)
        self.description_text.delete(1.0, tk.END)

        # Insert image
        photo = ImageTk.PhotoImage(image)
        self.description_text.image_create(tk.END, image=photo)

        # Update text widget and keep reference to photo
        self.description_text.config(state=tk.DISABLED)
        self.description_text.photo = photo

    def run(self):
        # Start the Tkinter main loop
        self.root.mainloop()


if __name__ == "__main__":
    # Create an instance of GetStartPage and run it
    get_start_page = GetStartPage()
    get_start_page.run()
