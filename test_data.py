import os
import unittest
from image_stress_analyzer import ImageStressAnalyzer
from sklearn.metrics import classification_report, accuracy_score

class TestImageStressAnalyzer(unittest.TestCase):
    def setUp(self):
        self.user_id = 0
        self.analyzer = ImageStressAnalyzer(self.user_id)
        self.test_images_dir = "Test_data"  # Set this to the directory containing your test images

        # Define ground truth for your test images
        self.ground_truth = {
            "photo_2.jpg": {"emotion": "neutral"},
            "photo_3.jpg": {"emotion": "neutral"},
            "photo_5.jpg": {"emotion": "happy"},
            "photo_6.jpg": {"emotion": "angry"},
            "photo_7.jpg": {"emotion": "angry"},
            "photo_8.jpg": {"emotion": "neutral"},
            "photo_9.jpg": {"emotion": "neutral"},
            "photo_10.jpg": {"emotion": "happy"},
            "photo_11.jpg": {"emotion": "neutral"},
            "photo_12.jpg": {"emotion": "neutral"},
            "photo_13.jpg": {"emotion": "happy"},
            "photo_14.jpg": {"emotion": "happy"},
            "photo_15.jpg": {"emotion": "neutral"},
            "photo_16.jpg": {"emotion": "neutral"},
            "photo_17.jpg": {"emotion": "happy"},
            "photo_18.jpg": {"emotion": "happy"},
            "photo_19.jpg": {"emotion": "surprise"},
            "photo_20.jpg": {"emotion": "sad"},
            "photo_21.jpg": {"emotion": "angry"},
            "photo_22.jpg": {"emotion": "surprise"},
            "photo_23.jpg": {"emotion": "angry"},
            "photo_24.jpg": {"emotion": "surprise"},
            "photo_25.jpg": {"emotion": "surprise"},
            "photo_26.jpg": {"emotion": "surprise"},
            "photo_27.jpg": {"emotion": "sad"},
            "photo_28.jpg": {"emotion": "sad"},
            "photo_29.jpg": {"emotion": "sad"},
            "photo_30.jpg": {"emotion": "sad"},
            "photo_31.jpg": {"emotion": "angry"},
            # Add all your images and their ground truth here
        }

        self.test_images = [os.path.join(self.test_images_dir, f) for f in self.ground_truth.keys()]

    def get_stress_level_range(self, emotion):
        # Define stress level ranges based on emotion
        emotion_to_range = {
            "neutral": (0.1, 0.3),
            "happy": (0.1, 0.3),
            "sad": (0.5, 0.7),
            "angry": (0.8, 1.0),
            "fear": (0.8, 1.0),
            "surprise": (0.4, 0.65)
        }
        return emotion_to_range.get(emotion, (0, 1))  # Default to (0, 1) if emotion is not listed

    def test_process_selected_image(self):
        total_images = len(self.test_images)
        y_true = []
        y_pred = []
        correct_stress_level = 0
        errors = []

        for img_path in self.test_images:
            with self.subTest(img_path=img_path):
                try:
                    filename = os.path.basename(img_path)
                    ground_truth_emotion = self.ground_truth[filename]["emotion"]
                    stress_level_range = self.get_stress_level_range(ground_truth_emotion)

                    emotion, stress_level = self.analyzer.process_selected_image(img_path)

                    y_true.append(ground_truth_emotion)
                    y_pred.append(emotion)

                    # Verify stress level detection (within a range)
                    if stress_level_range[0] <= stress_level <= stress_level_range[1]:
                        correct_stress_level += 1

                except Exception as e:
                    errors.append(f"Error processing {img_path}: {str(e)}")

        # Calculate accuracy metrics
        emotion_accuracy = accuracy_score(y_true, y_pred)
        stress_level_accuracy = correct_stress_level / total_images

        # Print classification report for emotion detection
        print(classification_report(y_true, y_pred))

        print(f"Overall Emotion Accuracy: {emotion_accuracy * 100:.2f}%")
        print(f"Stress Level Accuracy: {stress_level_accuracy * 100:.2f}%")

        # Print any errors encountered during processing
        if errors:
            print("\nErrors:")
            for error in errors:
                print(error)

        self.assertGreaterEqual(emotion_accuracy, 0.7, "Emotion recognition accuracy too low")
        self.assertGreaterEqual(stress_level_accuracy, 0.7, "Stress level estimation accuracy too low")


if __name__ == "__main__":
    unittest.main()
