from flask import Flask, render_template, Response, request, jsonify
import bicep_curl, plank, pushups, shoulder_press, squat, lateral_raise
import webbrowser
from flask_cors import CORS
from flask import Flask, send_from_directory
import socket
import firebase_admin # Import Firebase Admin SDK
from firebase_admin import credentials
from firebase_admin import db # Import db from firebase_admin
from firebase_utils import save_exercise
from datetime import datetime



app = Flask(__name__, static_folder='static')
CORS(app)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)
cred = credentials.Certificate("config/serviceAccountKey.json")  # Or "config/serviceAccountKey.json"
try:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://etmain-ac6d4-default-rtdb.firebaseio.com'  # Replace with your Firebase Realtime Database URL
    })
    firebase_db = db.reference()  # Get a reference to the database root
    print("Firebase Admin SDK initialized successfully!")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")
    #  Handle the error appropriately (e.g., exit, show a message)
    pass #  VERY important to handle this, so the rest of your app doesn't break.


# ✅ YouTube Video Dictionary
exercise_videos = {
    'bicep_curl': "HnHuhf4hEWY",
    'plank': "A2b2EmIg0dA",
    'pushups': "t0s5FHbdBmA",
    'shoulder_press': "Did01dFR3Lk",
    'squat': "YaXPRqUwItQ",
    'lateral_raise': "XPPfnSEATJA"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise/<exercise>')
def exercise_page(exercise):
    youtube_video_id = exercise_videos.get(exercise, "dQw4w9WgXcQ")  # Default video
    return render_template('exercise.html', exercise=exercise, youtube_video_id=youtube_video_id)

@app.route('/video_feed/<exercise>')
def video_feed(exercise):
    exercises = {
        'bicep_curl': bicep_curl.generate_frames,
        'plank': plank.generate_frames,
        'pushups': pushups.generate_frames,
        'shoulder_press': shoulder_press.generate_frames,
        'squat': squat.generate_frames,
        'lateral_raise': lateral_raise.generate_frames
    }

    if exercise in exercises:
        return Response(exercises[exercise](), mimetype='multipart/x-mixed-replace; boundary=frame')
    return "Exercise not found", 404

@app.route('/reset_count/<exercise>', methods=['POST'])
def reset_count(exercise):
    exercise_modules = {
        'bicep_curl': bicep_curl,
        'plank': plank,
        'pushups': pushups,
        'shoulder_press': shoulder_press,
        'squat': squat,
        'lateral_raise': lateral_raise
    }

    if exercise in exercise_modules:
        exercise_modules[exercise].reset_flag = True
        return jsonify({"success": True, "message": f"{exercise.capitalize()} count reset!"})
    
    return jsonify({"success": False, "message": "Invalid exercise"}), 400
@app.route('/get_count/<exercise>')
def get_count(exercise):
    exercise_modules = {
        'bicep_curl': bicep_curl,
        'plank': plank,
        'pushups': pushups,
        'shoulder_press': shoulder_press,
        'squat': squat,
        'lateral_raise': lateral_raise
    }
    if exercise in exercise_modules:
        return jsonify({'count': exercise_modules[exercise].current_count})
    return jsonify({'count': 0})

# --- NEW: Save exercise data live to Firebase ---
@app.route('/save_exercise/', methods=['POST'])
def save_exercise_route():
    data = request.get_json()
    user_id = data.get('user_id', 'default_user')  # Replace with actual user logic if available
    exercise_name = data.get('exercise_name')
    reps = data.get('reps')
    count = data.get('count')

    now = datetime.now()
    date = data.get('date', now.strftime('%Y-%m-%d'))
    day = data.get('day', now.strftime('%A'))
    time = data.get('time', now.strftime('%H:%M:%S'))

    try:
        save_exercise(user_id, exercise_name, reps, count, date, day, time)
        return jsonify({'success': True, 'message': 'Exercise saved!'})
    except Exception as e:
        print(f"Error saving exercise: {e}")
        return jsonify({'success': False, 'message': 'Failed to save exercise.'}), 500


if __name__ == '__main__':
    
    local_ip = socket.gethostbyname(socket.gethostname())  # Get your local IP
    webbrowser.open_new(f'http://{local_ip}:5000/')  # Open in browser
    print(f"✅ Flask app is running! Access it at: http://{local_ip}:5000/")
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5000)  # Listen on all IPs

