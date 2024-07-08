import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

import requests
from PIL import Image, ImageTk
import cv2
import dlib
import numpy as np
from deepface import DeepFace

from ipconfig import ip


class ImageStressAnalyzer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.root = tk.Tk()
        self.root.title("Image Stress Analysis")

        # Create and configure a main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create and configure labels with a larger font
        self.title_label = tk.Label(self.main_frame, text="Capture Your Image for Stress Analysis",
                                    font=("Helvetica", 18), pady=20)
        self.title_label.pack()

        # Create a label to display the user ID
        self.user_id_label = tk.Label(self.main_frame, text=f"User ID: {user_id}", font=("Helvetica", 12))
        self.user_id_label.pack()

        # Check if user is logged in
        if user_id == 0:
            self.user_id_label.config(text="User is not logged in")

        # Create a frame to contain the image labels
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack()

        # Create labels for the unprocessed and processed images
        self.unprocessed_label = tk.Label(self.image_frame, text="Unprocessed Image", font=("Helvetica", 14))
        self.unprocessed_label.grid(row=0, column=0, padx=20, pady=10)

        self.processed_label = tk.Label(self.image_frame, text="Processed Image with Facial Landmarks",
                                        font=("Helvetica", 14))
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

        # Initialize Dlib's face detector and landmark predictor
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_detector = dlib.shape_predictor("data/shape_predictor_68_face_landmarks.dat")

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

        messagebox.showinfo("Position Yourself",
                            "Position yourself properly and press the spacebar to capture the image.")

        while True:
            ret, frame = cap.read()

            if not ret:
                messagebox.showerror("Error", "Failed to capture image from the webcam.")
                break

            # Display the frame in a window (optional)
            cv2.imshow("Capture Frame", frame)

            key = cv2.waitKey(1)
            if key == 32:  # Spacebar key code
                # Generate a unique filename based on current timestamp and user ID
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                file_name = f"captured_image_user_{self.user_id}_{timestamp}.jpg"
                file_path = os.path.join("captured_images", file_name)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                cv2.imwrite(file_path, frame)  # Save the captured image locally
                cap.release()
                cv2.destroyAllWindows()

                # Process the captured image and retrieve emotion and stress level
                emotion, stress_level = self.process_selected_image(file_path)

                # Check if user is logged in before prompting to save to database
                if self.user_id == 0:
                    messagebox.showinfo("Save to Database",
                                        "User is not logged in. Analysis result can only be viewed.")
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
            faces = self.face_detector(gray_frame)

            emotion_label = 'neutral'
            stress_level = 0.0

            for face in faces:
                landmarks = self.landmark_detector(gray_frame, face)

                # Draw facial landmarks on the image with larger circles
                for i in range(68):  # Assuming you're using the 68-point facial landmarks model
                    x, y = landmarks.part(i).x, landmarks.part(i).y
                    cv2.circle(image_cv2, (x, y), 2, (0, 255, 0), -1)  # Larger circles

                # Detect faces and predict emotions using DeepFace
                face_roi = image_cv2[face.top():face.bottom(), face.left():face.right()]
                result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

                # Check if 'dominant_emotion' key exists in result
                if 'dominant_emotion' in result[0]:
                    emotion_label = result[0]['dominant_emotion']
                else:
                    raise ValueError("Unable to detect emotion from the provided image.")

                # Display emotion label on the image
                cv2.putText(image_cv2, emotion_label, (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

                # Estimate stress level based on facial landmarks and emotion label
                stress_level = self.estimate_stress_level(landmarks, emotion_label)

            # Display the processed image with facial landmarks
            processed_image_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
            processed_image = ImageTk.PhotoImage(processed_image_pil)
            self.processed_image_label.config(image=processed_image)
            self.processed_image_label.image = processed_image

            # Display analysis results in a message box
            result_message = (f"Emotion: {emotion_label}\nStress Level: {stress_level:.2f}\nDo you want to save the "
                              f"analysis result?")

            if self.user_id != 0 and messagebox.askyesno("Analysis Results", result_message):
                # If the user is logged in and chooses to save the analysis result, send data to backend
                with open(file_path, "rb") as image_file:
                    image_data = image_file.read()
                self.send_analysis_result_to_backend(image_data, emotion_label, stress_level)
            else:
                messagebox.showinfo("Analysis Results", f"Emotion: {emotion_label}\nStress Level: {stress_level:.2f}")

            return emotion_label, stress_level

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the image: {str(e)}")
            return None, None

    def estimate_stress_level(self, landmarks, emotion_label):
        # Calculate individual features based on landmarks
        brow_furrow = self.calculate_brow_furrow(landmarks)
        jaw_tension = self.calculate_jaw_tension(landmarks)
        eye_expression = self.calculate_eye_expression(landmarks)
        mouth_shape = self.calculate_mouth_shape(landmarks)

        # Normalize the calculated features to be between 0 and 1
        brow_furrow = np.clip(brow_furrow / 10.0, 0, 1)
        jaw_tension = np.clip(jaw_tension / 20.0, 0, 1)
        eye_expression = np.clip(eye_expression / 15.0, 0, 1)
        mouth_shape = np.clip(mouth_shape / 15.0, 0, 1)

        # Aggregate the normalized features
        landmark_stress_level = (brow_furrow + jaw_tension + eye_expression + mouth_shape) / 4.0

        # Base emotion stress level, initially neutral
        emotion_stress_level = 0.0

        # Adjust stress level based on predicted emotion
        emotion_adjustments = {
            'angry': 0.8,
            'fear': 0.75,
            'sad': 0.5,
            'surprise': 0.35,
            'disgust': 0.20,
            'neutral': 0.05,
            'happy': 0.00,

        }

        emotion_label_lower = emotion_label.lower()
        if emotion_label_lower in emotion_adjustments:
            emotion_stress_level += emotion_adjustments[emotion_label_lower]

        # Combine landmark stress level and emotion stress level with respective weights
        combined_stress_level = (0.2 * landmark_stress_level) + (0.8 * emotion_stress_level)

        return combined_stress_level

    def calculate_brow_furrow(self, landmarks):
        left_brow = (landmarks.part(21).x, landmarks.part(21).y)
        right_brow = (landmarks.part(22).x, landmarks.part(22).y)
        brow_distance = np.linalg.norm(np.array(left_brow) - np.array(right_brow))
        return brow_distance

    def calculate_jaw_tension(self, landmarks):
        left_jaw = (landmarks.part(3).x, landmarks.part(3).y)
        right_jaw = (landmarks.part(13).x, landmarks.part(13).y)
        jaw_distance = np.linalg.norm(np.array(left_jaw) - np.array(right_jaw))
        return jaw_distance

    def calculate_eye_expression(self, landmarks):
        left_eye = (landmarks.part(37).y, landmarks.part(41).y)
        right_eye = (landmarks.part(43).y, landmarks.part(47).y)
        left_eye_openness = np.abs(left_eye[0] - left_eye[1])
        right_eye_openness = np.abs(right_eye[0] - right_eye[1])
        eye_openness = (left_eye_openness + right_eye_openness) / 2.0
        return eye_openness

    def calculate_mouth_shape(self, landmarks):
        top_lip = landmarks.part(51).y
        bottom_lip = landmarks.part(57).y
        mouth_openness = np.abs(top_lip - bottom_lip)
        return mouth_openness

    def send_analysis_result_to_backend(self, image_data, emotion, stress_level):
        # URL of the PHP backend script
        url = "http://" + ip + "/fsia/save_analysis.php"

        # Prepare the data to be sent
        data = {
            "user_id": self.user_id,
            "image_data": image_data,  # You may need to convert image_data to a suitable format
            "emotion": emotion,
            "stress_level": stress_level
        }

        # Send an HTTP POST request to the PHP backend
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                print("Analysis results sent to backend successfully.")
            else:
                print("Failed to send analysis results to backend.")
        except Exception as e:
            print(f"An error occurred while sending data to backend: {e}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    # Retrieve user ID from command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python image_stress_analyzer.py <user_id>")
        sys.exit(1)

    try:
        user_id = int(sys.argv[1])
    except ValueError:
        print("Error: User ID must be an integer.")
        sys.exit(1)

    app = ImageStressAnalyzer(user_id)
    app.run()
