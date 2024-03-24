import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
import re

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration")

        # Load background image
        background_image = Image.open("img/registration.jpg")
        background_photo = ImageTk.PhotoImage(background_image)

        # Create a canvas to place the background image
        canvas = tk.Canvas(self.root, width=1000, height=650)
        canvas.pack(fill="both", expand=True)

        # Place the background image on the canvas
        canvas.create_image(0, 0, anchor="nw", image=background_photo)
        canvas.image = background_photo  # Keep a reference to avoid garbage collection

        # Registration frame
        register_frame = ttk.Frame(canvas, padding="30")
        register_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        title_label = ttk.Label(register_frame, text="Registration", font=("Helvetica", 22, "bold"), foreground="black")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Common style for labels and entries
        label_style = {"font": ("Georgia", 10), "foreground": "black"}
        entry_style = {"font": ("Helvetica", 10), "background": "white", "foreground": "black"}

        # Define icon size
        icon_size = (15, 18)  # Change icon size

        # Username input with icon
        self.username_icon = self.load_image("img/username_icon.png", icon_size)
        self.username_label = ttk.Label(register_frame, text=" Username:", **label_style)
        self.username_label.config(image=self.username_icon, compound=tk.LEFT)
        self.username_label.grid(row=1, column=0, sticky="w", padx=(0, 10))

        self.username_entry = ttk.Entry(register_frame, **entry_style)
        self.username_entry.grid(row=1, column=1, pady=(0, 10), padx=(0, 50), sticky="we")
        self.username_entry.focus()

        # Phone number input with icon
        self.phone_icon = self.load_image("img/phone_icon.png", icon_size)
        self.phone_label = ttk.Label(register_frame, text=" Phone Number:", **label_style)
        self.phone_label.config(image=self.phone_icon, compound=tk.LEFT)
        self.phone_label.grid(row=2, column=0, sticky="w", padx=(0, 10))

        self.phone_entry = ttk.Entry(register_frame, **entry_style)
        self.phone_entry.grid(row=2, column=1, pady=(0, 10), padx=(0, 50), sticky="we")

        # Email input with icon
        self.email_icon = self.load_image("img/email_icon.png", icon_size)
        self.email_label = ttk.Label(register_frame, text=" Email:", **label_style)
        self.email_label.config(image=self.email_icon, compound=tk.LEFT)
        self.email_label.grid(row=3, column=0, sticky="w", padx=(0, 10))

        self.email_entry = ttk.Entry(register_frame, **entry_style)
        self.email_entry.grid(row=3, column=1, pady=(0, 10), padx=(0, 50), sticky="we")

        # Password input with icon
        self.password_icon = self.load_image("img/password_icon.png", icon_size)
        self.password_label = ttk.Label(register_frame, text=" Password:", **label_style)
        self.password_label.config(image=self.password_icon, compound=tk.LEFT)
        self.password_label.grid(row=4, column=0, sticky="w", padx=(0, 10))

        self.password_entry = ttk.Entry(register_frame, show="*", **entry_style)
        self.password_entry.grid(row=4, column=1, pady=(0, 10), padx=(0, 50), sticky="we")

        # Confirm Password input with icon
        confirm_password_label = ttk.Label(register_frame, text=" Confirm Password: ", **label_style)
        confirm_password_label.config(image=self.password_icon, compound=tk.LEFT)
        confirm_password_label.grid(row=5, column=0, sticky="w", padx=(0, 10))

        self.confirm_password_entry = ttk.Entry(register_frame, show="*", **entry_style)
        self.confirm_password_entry.grid(row=5, column=1, pady=(0, 10), padx=(0, 50), sticky="we")

        # Register button
        register_button = ttk.Button(register_frame, text=" Register ", command=self.register)
        register_button.grid(row=6, column=0, columnspan=2, pady=(0, 20))

    def load_image(self, path, size):
        try:
            image = Image.open(path)
            image = image.resize(size)
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            print(f"Error: Image not found at {path}")
            return None

    def register(self):
        # Retrieve data from entry fields
        user_name = self.username_entry.get()
        user_phone = self.phone_entry.get()
        user_email = self.email_entry.get()
        user_password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Validation
        if not user_name or not user_phone or not user_email or not user_password or not confirm_password:
            messagebox.showerror("Error", "All fields are required.")
            return

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", user_email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        if len(user_phone) != 10 or not user_phone.isdigit():
            messagebox.showerror("Error", "Invalid phone number.")
            return

        if user_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return

        # Send data to PHP script
        url = "http://192.168.0.104/fsia/register.php"
        data = {
            'user_name': user_name,
            'user_phone': user_phone,
            'user_email': user_email,
            'user_password': user_password
        }
        response = requests.post(url, data=data)

        if response.text == "Registration successful":
            messagebox.showinfo("Success", "Registration successful.")
            # Clear entry fields after successful registration
            self.username_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.confirm_password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", response.text)

# Create and run the registration window
if __name__ == "__main__":
    root = tk.Tk()
    RegisterWindow(root)
    root.mainloop()
