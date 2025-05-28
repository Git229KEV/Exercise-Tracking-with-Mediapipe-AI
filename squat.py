# squat.py

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
    """✅ Reset the squat counter"""
    global counter, reset_flag
    counter = 0
    reset_flag = False  # ✅ Reset flag after updating

def generate_frames():
    global counter, stage, reset_flag
    cap = cv2.VideoCapture(0)

    # ✅ Increase confidence threshold to detect squats better
    with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # ✅ Reset count if flag is set
            if reset_flag:
                reset_counter()

            frame = cv2.flip(frame, 1)  # Mirror effect
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
                knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
                hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]

                # ✅ Squat detection logic
                if knee.y > hip.y:
                    stage = "DOWN"
                elif knee.y < hip.y and stage == "DOWN":
                    stage = "UP"
                    counter += 1

            # ✅ Display count on frame
            cv2.putText(frame, f"Squats: {counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Stage: {stage}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # ✅ Encode frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
