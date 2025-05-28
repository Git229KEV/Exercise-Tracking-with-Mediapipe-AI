import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

counter = 0
stage = None
reset_flag = False  # ✅ Reset flag

def reset_counter():
    global counter, reset_flag
    counter = 0
    reset_flag = False  # ✅ Reset flag after updating

def generate_frames():
    global counter, stage, reset_flag
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            if reset_flag:
                reset_counter()

            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            try:
                landmarks = results.pose_landmarks.landmark
                shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
                hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]

                if shoulder.y < hip.y:
                    stage = "UP"
                else:
                    stage = "DOWN"
                    counter += 1

            except Exception as e:
                print(f"Error: {e}")

            cv2.putText(frame, f"Counter: {counter}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
