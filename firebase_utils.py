import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase only once
cred = credentials.Certificate('config/serviceAccountKey.json')
try:
    firebase_admin.get_app()
except ValueError:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://etmain-ac6d4-default-rtdb.firebaseio.com'
    })

def save_exercise(user_id, exercise_name, reps, sets, date=None, day=None, time=None):
    """
    Save exercise details to Firebase Realtime Database.
    """
    now = datetime.now()
    date = date or now.strftime('%Y-%m-%d')
    day = day or now.strftime('%A')
    time = time or now.strftime('%H:%M:%S')

    exercise_data = {
        'exercise_name': exercise_name,
        'reps': reps,
        'sets': sets,
        'date': date,
        'day': day,
        'time': time,
        'timestamp': now.isoformat()
    }

    # Store under user's exercises path for scalability
    ref = db.reference(f'/users/{user_id}/exercises')
    ref.push(exercise_data)
