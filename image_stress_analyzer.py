import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np
from PIL import Image, ImageTk
import cv2
import dlib
from deepface import DeepFace

class ImageStressAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Stress Analysis")

        # Create and configure a main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create and configure labels with a larger font
        self.title_label = tk.Label(self.main_frame, text="Capture Your Image for Stress Analysis", font=("Helvetica", 18), pady=20)
        self.title_label.pack()

        # Create a frame to contain the image labels
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack()

        # Create labels for the unprocessed and processed images
        self.unprocessed_label = tk.Label(self.image_frame, text="Unprocessed Image", font=("Helvetica", 14))
        self.unprocessed_label.grid(row=0, column=0, padx=20, pady=10)

        self.processed_label = tk.Label(self.image_frame, text="Processed Image with Facial Landmarks", font=("Helvetica", 14))
        self.processed_label.grid(row=0, column=1, padx=20, pady=10)

        # Create labels for the unprocessed and processed images
        self.unprocessed_image_label = tk.Label(self.image_frame, bd=2, relief="solid", padx=5, pady=5)
        self.unprocessed_image_label.grid(row=1, column=0, padx=20, pady=10)

        self.processed_image_label = tk.Label(self.image_frame, bd=2, relief="solid", padx=5, pady=5)
        self.processed_image_label.grid(row=1, column=1, padx=20, pady=10)

        # Create and configure buttons
        self.upload_button = tk.Button(self.main_frame, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=10)

        self.capture_button = tk.Button(self.main_frame, text="Capture Image", command=self.capture_image)
        self.capture_button.pack(pady=10)

        # Initialize DeepFace model for emotion analysis
        self.emotion_model = DeepFace.build_model("Emotion")
        self.emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

        # Initialize facial landmark detector from dlib
        self.landmark_detector = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # Load and display the dummy images for placeholders
        self.dummy_image_left = Image.open("img/upload.jpg")
        self.dummy_image_left = self.dummy_image_left.resize((430, 500), Image.LANCZOS)
        self.dummy_image_left = ImageTk.PhotoImage(self.dummy_image_left)
        self.unprocessed_image_label.config(image=self.dummy_image_left)

        self.dummy_image_right = Image.open("img/facial.jpg")
        self.dummy_image_right = self.dummy_image_right.resize((430, 500), Image.LANCZOS)
        self.dummy_image_right = ImageTk.PhotoImage(self.dummy_image_right)
        self.processed_image_label.config(image=self.dummy_image_right)

    def upload_image(self):
        file_path = filedialog.askopenfilename(title="Select Your Image",
                                               filetypes=[("Image files", "*.jpg *.png *.jpeg")])

        if file_path:
            self.process_selected_image(file_path)

    def capture_image(self):
        # Open a simple dialog to choose the camera (assuming one built-in camera)
        camera_index = 0

        cap = cv2.VideoCapture(camera_index)

        messagebox.showinfo("Position Yourself", "Position yourself properly and press the spacebar to capture the image.")

        while True:
            ret, frame = cap.read()

            if not ret:
                messagebox.showerror("Error", "Failed to capture image from the webcam.")
                break

            # Display the frame in a window (optional)
            cv2.imshow("Capture Frame", frame)

            key = cv2.waitKey(1)
            if key == 32:  # Spacebar key code
                cv2.imwrite("captured_image.jpg", frame)
                cap.release()
                cv2.destroyAllWindows()
                self.process_selected_image("captured_image.jpg")
                break

        cap.release()

    def process_selected_image(self, file_path):
        try:
            # Load and display the selected image (unprocessed)
            image_pil = Image.open(file_path)
            if image_pil is None or image_pil.size[0] == 0 or image_pil.size[1] == 0:
                raise ValueError("Failed to load the image or the image is empty.")

            image_pil = image_pil.resize((430, 500), Image.LANCZOS)
            unprocessed_image = ImageTk.PhotoImage(image_pil)
            self.unprocessed_image_label.config(image=unprocessed_image)
            self.unprocessed_image_label.image = unprocessed_image

            # Convert PIL image to OpenCV format
            image_cv2 = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

            # Process the image with facial landmarks
            gray_frame = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                dlib_rect = dlib.rectangle(x, y, x + w, y + h)
                landmarks = self.landmark_detector(gray_frame, dlib_rect)

                # Draw facial landmarks on the image with larger circles
                for i in range(68):  # Assuming you're using the 68-point facial landmarks model
                    x, y = landmarks.part(i).x, landmarks.part(i).y
                    cv2.circle(image_cv2, (x, y), 2, (0, 255, 0), -1)  # Larger circles

            # Display the processed image with facial landmarks
            processed_image_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
            processed_image = ImageTk.PhotoImage(processed_image_pil)
            self.processed_image_label.config(image=processed_image)
            self.processed_image_label.image = processed_image

            # Example emotion analysis code (you can customize this)
            resized_face = cv2.resize(gray_frame, (48, 48), interpolation=cv2.INTER_AREA)
            normalized_face = resized_face / 255.0
            reshaped_face = normalized_face.reshape(1, 48, 48, 1)
            preds = self.emotion_model.predict(reshaped_face)[0]
            emotion_idx = preds.argmax()
            emotion = self.emotion_labels[emotion_idx]
            stress_level = 1.0 - (preds[3] + preds[6])

            # Display analysis results in a message box
            messagebox.showinfo("Analysis Results", f"Emotion: {emotion}\nStress Level: {stress_level:.2f}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageStressAnalyzer()
    app.run()
