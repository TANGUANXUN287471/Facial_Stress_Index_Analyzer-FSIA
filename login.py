import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        # Load background image
        background_image = Image.open("img/registration.jpg")
        self.background_photo = ImageTk.PhotoImage(background_image)

        # Create a canvas to place the background image
        self.canvas = tk.Canvas(self.root, width=1000, height=650)
        self.canvas.pack(fill="both", expand=True)

        # Place the background image on the canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Login frame
        self.login_frame = ttk.Frame(self.canvas, padding="30")
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title label
        title_label = ttk.Label(self.login_frame, text="Login", font=("Helvetica", 22, "bold"), foreground="black")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Common style for labels and entries
        label_style = {"font": ("Georgia", 10), "foreground": "black"}
        entry_style = {"font": ("Helvetica", 10), "background": "white", "foreground": "black"}

        # Define icon size
        icon_size = (15, 18)  # Change icon size

        # Email input
        email_icon = Image.open("img/email_icon.png").resize((15, 18))
        self.email_icon_photo = ImageTk.PhotoImage(email_icon)
        email_icon_label = ttk.Label(self.login_frame, image=self.email_icon_photo)
        email_icon_label.grid(row=1, column=0, sticky="e", padx=(0, 10))

        email_label = ttk.Label(self.login_frame, text="Email:", **label_style)
        email_label.grid(row=1, column=1, sticky="w")

        self.email_entry = ttk.Entry(self.login_frame, **entry_style)
        self.email_entry.grid(row=1, column=2, pady=(0, 10), padx=(0, 50), sticky="we")
        self.email_entry.focus()

        # Password input
        password_icon = Image.open("img/password_icon.png").resize((15, 18))
        self.password_icon_photo = ImageTk.PhotoImage(password_icon)
        password_icon_label = ttk.Label(self.login_frame, image=self.password_icon_photo)
        password_icon_label.grid(row=2, column=0, sticky="e", padx=(0, 10))

        password_label = ttk.Label(self.login_frame, text="Password:", **label_style)
        password_label.grid(row=2, column=1, sticky="w")

        self.password_entry = ttk.Entry(self.login_frame, show="*", **entry_style)
        self.password_entry.grid(row=2, column=2, pady=(0, 10), padx=(0, 50), sticky="we")

        # Login button
        login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=0, columnspan=3, pady=(0, 20))

    def login(self):
        # Retrieve data from entry fields
        user_email = self.email_entry.get()
        user_password = self.password_entry.get()

        # Validation
        if not user_email or not user_password:
            messagebox.showerror("Error", "Please enter both email and password.")
            return

        # Send data to PHP script
        url = "http://192.168.0.104/fsia/login.php"
        data = {
            'user_email': user_email,
            'user_password': user_password
        }
        response = requests.post(url, data=data)

        if response.text == "Login successful":
            messagebox.showinfo("Success", "Login successful.")
            # Clear entry fields after successful login
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", response.text)

# Create and run the login window
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
