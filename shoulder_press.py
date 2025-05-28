# shoulder_press.py

import cv2
import mediapipe as mp

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Global Variables
counter = 0
stage = None
reset_flag = False  # ✅ Reset flag

def reset_counter():
    """✅ Reset the shoulder press counter"""
    global counter, reset_flag, stage
    counter = 0
    stage = None  # ✅ Reset stage to avoid instant counting
    reset_flag = False  # ✅ Reset flag after updating

def generate_frames():
    global counter, stage, reset_flag
    cap = cv2.VideoCapture(0)

    # ✅ Increase confidence threshold for better accuracy
    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # ✅ Reset count if flag is set
            if reset_flag:
                reset_counter()

            frame = cv2.flip(frame, 1)  # ✅ Mirror effect
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # ✅ Make pose detection
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                # ✅ Draw pose landmarks
                mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
                )

                # ✅ Extract key landmarks
                landmarks = results.pose_landmarks.landmark
                wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
                shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]

                # ✅ Corrected counting logic:
                # Wrist must be **above** the shoulder for "UP" stage
                if wrist.y < shoulder.y and elbow.y < shoulder.y:
                    stage = "UP"

                # Wrist must be **below** the shoulder for "DOWN" stage
                elif wrist.y > shoulder.y and elbow.y > shoulder.y and stage == "UP":
                    stage = "DOWN"
                    counter += 1  # ✅ Count only when moving **down** after "UP"

            # ✅ Display counter & stage
            cv2.putText(frame, f"Shoulder Press: {counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Stage: {stage}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # ✅ Encode frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
