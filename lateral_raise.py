import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Global Variables
raise_count = 0
is_raising = False
reset_flag = False  # ✅ Reset flag

def reset_counter():
    """✅ Reset the lateral raise counter"""
    global raise_count, reset_flag, is_raising
    raise_count = 0
    is_raising = False
    reset_flag = False  # ✅ Reset flag after updating

# Function to calculate angle between three points
def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    radians = np.arccos(np.clip(
        np.dot(b - a, c - b) / (np.linalg.norm(b - a) * np.linalg.norm(c - b)),
        -1.0, 1.0))
    angle = np.degrees(radians)
    return angle

def generate_frames():
    global raise_count, is_raising, reset_flag
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ ERROR: Camera not opening! Check if another program is using it.")
        return

    with mp_pose.Pose(model_complexity=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        prev_left_angle = None
        prev_right_angle = None

        while cap.isOpened():
            ret, image = cap.read()
            if not ret:
                print("❌ ERROR: Unable to read frame. Exiting...")
                break  # ✅ Prevents infinite loop if camera fails

            # ✅ Reset count if flag is set
            if reset_flag:
                reset_counter()

            # Mirror image & convert to RGB
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
                left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
                left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
                left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
                right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
                right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]

                # ✅ Calculate angles
                left_angle = calculate_angle(left_shoulder, left_elbow, left_hip)
                right_angle = calculate_angle(right_shoulder, right_elbow, right_hip)

                # ✅ Prevent false positives (better threshold)
                if prev_left_angle is not None and prev_right_angle is not None:
                    left_delta = abs(left_angle - prev_left_angle)
                    right_delta = abs(right_angle - prev_right_angle)

                    if not is_raising and left_delta > 15 and right_delta > 15:
                        is_raising = True
                    elif is_raising and left_delta < 5 and right_delta < 5:
                        is_raising = False
                        if left_angle > 120 and right_angle > 120:
                            raise_count += 1  # ✅ Count only after full motion

                prev_left_angle = left_angle
                prev_right_angle = right_angle

            # ✅ Display lateral raise count on frame
            cv2.putText(image, f'Lateral Raises: {raise_count}', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # ✅ Encode frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', image)
            if not ret:
                print("❌ ERROR: Frame encoding failed!")
                break  # ✅ Prevents sending corrupted frames

            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
