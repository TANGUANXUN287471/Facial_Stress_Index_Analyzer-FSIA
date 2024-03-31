import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import dlib
import numpy as np
from keras.models import load_model


class ImageStressAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Stress Analysis")

        # Create and configure a main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create and configure labels with a larger font
        self.title_label = tk.Label(self.main_frame, text="Capture Your Image for Stress Analysis",
                                    font=("Helvetica", 18), pady=20)
        self.title_label.pack()

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

        # Initialize facial landmark detector from dlib
        self.landmark_detector = dlib.shape_predictor("data/shape_predictor_68_face_landmarks (1).dat")

        # Load and display the dummy images for placeholders
        self.dummy_image_left = Image.open("img/upload.jpg")
        self.dummy_image_left = self.dummy_image_left.resize((430, 500), Image.LANCZOS)
        self.dummy_image_left = ImageTk.PhotoImage(self.dummy_image_left)
        self.unprocessed_image_label.config(image=self.dummy_image_left)

        self.dummy_image_right = Image.open("img/facial.jpg")
        self.dummy_image_right = self.dummy_image_right.resize((430, 500), Image.LANCZOS)
        self.dummy_image_right = ImageTk.PhotoImage(self.dummy_image_right)
        self.processed_image_label.config(image=self.dummy_image_right)

        # Load emotion recognition model
        self.emotion_model = load_model("fer2013_mini_XCEPTION.119-0.65.hdf5")

        # Emotion labels
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

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

            # Detect faces and predict emotions
            faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            for (x, y, w, h) in faces:
                face_roi = gray_frame[y:y + h, x:x + w]
                resized_roi = cv2.resize(face_roi, (48, 48))
                normalized_roi = resized_roi / 255.0
                reshaped_roi = np.expand_dims(np.expand_dims(normalized_roi, -1), 0)
                predictions = self.emotion_model.predict(reshaped_roi)
                emotion_label = self.emotion_labels[np.argmax(predictions)]

                # Display emotion label on the image
                cv2.putText(image_cv2, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

                # Estimate stress level based on facial landmarks and emotion label
                stress_level = self.estimate_stress_level(landmarks, emotion_label)

            # Display the processed image with emotion labels
            processed_image_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
            processed_image = ImageTk.PhotoImage(processed_image_pil)
            self.processed_image_label.config(image=processed_image)
            self.processed_image_label.image = processed_image

            # Display analysis results in a message box
            messagebox.showinfo("Analysis Results", f"Emotion: {emotion_label}\nStress Level: {stress_level:.2f}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def estimate_stress_level(self, landmarks, emotion_label):
        # Define weights for different facial landmarks based on their relevance to stress
        weights = {
            'brow_furrow': 0.25,
            'jaw_tension': 0.25,
            'eye_expression': 0.25,
            'mouth_shape': 0.25
        }

        # Initialize stress level
        stress_level = 0.0

        # Calculate stress level based on facial landmarks
        # 1. Brow Furrow
        brow_furrow = self.calculate_brow_furrow(landmarks)
        stress_level += weights['brow_furrow'] * brow_furrow

        # 2. Jaw Tension
        jaw_tension = self.calculate_jaw_tension(landmarks)
        stress_level += weights['jaw_tension'] * jaw_tension

        # 3. Eye Expression
        eye_expression = self.calculate_eye_expression(landmarks)
        stress_level += weights['eye_expression'] * eye_expression

        # 4. Mouth Shape
        mouth_shape = self.calculate_mouth_shape(landmarks)
        stress_level += weights['mouth_shape'] * mouth_shape

        # Adjust stress level based on predicted emotion
        if emotion_label in ['Angry', 'Fear']:
            stress_level += 0.7  # Increase stress level for negative emotions
        elif emotion_label == 'Sad':
            stress_level += 0.5
        elif emotion_label == 'Surprise':
            stress_level += 0.3  # Slight increase for surprise
        elif emotion_label == 'Disgust':
            stress_level += 0.15
        elif emotion_label in ['Happy', 'Neutral']:
            stress_level += 0.0

        return stress_level

    def calculate_brow_furrow(self, landmarks):
        # Calculate brow furrow based on the distance between eyebrow landmarks
        left_eyebrow = [landmarks.part(i) for i in range(17, 22)]  # Left eyebrow landmarks
        right_eyebrow = [landmarks.part(i) for i in range(22, 27)]  # Right eyebrow landmarks

        # Calculate the distance between the endpoints of left and right eyebrows
        left_eyebrow_end = np.array([left_eyebrow[0].x, left_eyebrow[0].y])
        right_eyebrow_start = np.array([right_eyebrow[0].x, right_eyebrow[0].y])
        brow_furrow_distance = np.linalg.norm(left_eyebrow_end - right_eyebrow_start)

        # Normalize the distance to a scale of 0 to 1
        normalized_distance = brow_furrow_distance / landmarks.rect.width()

        # Map the normalized distance to the stress level range (0 to 1)
        stress_level = 1.0 - normalized_distance

        return stress_level

    def calculate_jaw_tension(self, landmarks):
        # Calculate jaw tension based on the distance between jawline landmarks
        jaw_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(0, 17)]

        # Calculate the distances between consecutive jawline points
        jaw_distances = [np.linalg.norm(np.array(jaw_points[i]) - np.array(jaw_points[i + 1])) for i in range(16)]

        # Average the distances to get jaw tension
        jaw_tension = np.mean(jaw_distances)

        # Normalize the jaw tension to a scale of 0 to 1
        normalized_tension = jaw_tension / landmarks.rect.width()

        return normalized_tension

    def calculate_eye_expression(self, landmarks):
        # Calculate eye expression based on the position of eye landmarks
        left_eye_openness = landmarks.part(42).y - landmarks.part(38).y
        right_eye_openness = landmarks.part(47).y - landmarks.part(43).y

        # Average the eye openness values
        eye_expression = (left_eye_openness + right_eye_openness) / 2

        # Normalize eye expression to a scale of 0 to 1
        normalized_expression = eye_expression / landmarks.rect.height()

        return normalized_expression

    def calculate_mouth_shape(self, landmarks):
        # Calculate mouth shape based on the position of mouth landmarks
        mouth_width = landmarks.part(54).x - landmarks.part(48).x
        mouth_height = (landmarks.part(66).y - landmarks.part(62).y +
                        landmarks.part(57).y - landmarks.part(60).y) / 2

        # Calculate the area of the mouth rectangle
        mouth_area = mouth_width * mouth_height

        # Normalize mouth area to a scale of 0 to 1
        normalized_area = mouth_area / (landmarks.rect.width() * landmarks.rect.height())

        return normalized_area

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ImageStressAnalyzer()
    app.run()
