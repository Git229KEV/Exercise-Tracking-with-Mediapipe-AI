import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Global Variables
push_up_count = 0
push_up_start = False
reset_flag = False  # ✅ Reset flag

def reset_counter():
    """✅ Reset the push-up counter"""
    global push_up_count, reset_flag, push_up_start
    push_up_count = 0
    push_up_start = False
    reset_flag = False  # ✅ Reset flag after updating

# Function to calculate distance between two points
def distance_calculate(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

def generate_frames():
    global push_up_count, push_up_start, reset_flag
    cap = cv2.VideoCapture(0)

    # ✅ Increase detection confidence for better tracking
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            ret, image = cap.read()
            if not ret:
                break

            # ✅ Reset count if flag is set
            if reset_flag:
                reset_counter()

            # Flip image for correct selfie-view
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            results = pose.process(image_rgb)

            if results.pose_landmarks:
                # ✅ Draw pose landmarks
                mp_drawing.draw_landmarks(
                    image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                )

                # ✅ Extract key landmarks
                landmarks = results.pose_landmarks.landmark
                image_height, image_width, _ = image.shape

                right_shoulder = (int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width),
                                  int(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height))
                right_wrist = (int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width),
                               int(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height))

                # ✅ Fix counting logic to avoid continuous counting:
                if distance_calculate(right_shoulder, right_wrist) < 130:
                    push_up_start = True
                elif push_up_start and distance_calculate(right_shoulder, right_wrist) > 250:
                    push_up_count += 1
                    push_up_start = False  # ✅ Ensure only one count per rep

            # ✅ Display counter on frame
            cv2.putText(image, f"Push-ups: {push_up_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # ✅ Encode frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

    cap.release()
