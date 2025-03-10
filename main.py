import cv2
import dlib
import time
import datetime
import sqlite3
import numpy as np

# Initialize the database
def create_database():
    conn = sqlite3.connect('facial_data.db')
    c = conn.cursor()
    # Create a table for storing face data and landmarks
    c.execute('''CREATE TABLE IF NOT EXISTS face_data (
                    face_id INTEGER PRIMARY KEY,
                    timestamp TEXT,
                    landmarks TEXT)''')
    conn.commit()
    conn.close()

# Function to insert face data and landmarks into the database
def insert_face_data(face_id, timestamp, landmarks):
    conn = sqlite3.connect('facial_data.db')
    c = conn.cursor()
    landmarks_str = ",".join(map(str, landmarks))  # Store landmarks as comma-separated string
    c.execute('INSERT INTO face_data (face_id, timestamp, landmarks) VALUES (?, ?, ?)', 
              (face_id, timestamp, landmarks_str))
    conn.commit()
    conn.close()

# Function to check if a face with the same landmarks already exists in the database
def is_face_in_database(landmarks, tolerance=50):
    conn = sqlite3.connect('facial_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM face_data')
    rows = c.fetchall()
    conn.close()

    # Compare the incoming landmarks with those stored in the database
    for row in rows:
        stored_landmarks = list(map(float, row[2].split(',')))  # Convert stored landmarks to float
        distance = np.linalg.norm(np.array(stored_landmarks) - np.array(landmarks))  # Euclidean distance

        if distance < tolerance:  # If the distance is within the tolerance, it's the same face
            return True, row[0]  # Return True and the existing face_id
    return False, None

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

# Load dlib's facial landmark predictor
predictor_path = "shape_predictor_68_face_landmarks/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

create_database()  # Create database to store face data and landmarks

face_counter = 0  # to keep track of unique face ids
SECONDS_TO_RECORD_AFTER_DETECTION = 10  # How long to continue recording after detection
detection = False
timer_started = False
detection_stopped_time = None
out = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Detect faces and extract landmarks
    dlib_faces = detector(gray)
    for face in dlib_faces:
        landmarks = predictor(gray, face)
        
        # Extract the 68 facial landmark coordinates
        face_landmarks = np.array([[landmarks.part(n).x, landmarks.part(n).y] for n in range(68)])
        face_landmarks_flattened = face_landmarks.flatten()  # Flatten to a 1D array for storage

        # Check if this face has been seen before by comparing landmarks with tolerance
        is_seen, existing_face_id = is_face_in_database(face_landmarks_flattened)
        
        if not is_seen:
            # New face detected, assign new face_id and insert data into database
            face_counter += 1
            timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            insert_face_data(face_counter, timestamp, face_landmarks_flattened)
            print(f"Face {face_counter} first detected at {timestamp}")
        else:
            print(f"Face already seen. Existing Face ID: {existing_face_id}")

        # Draw the landmarks on the frame
        for (x, y) in face_landmarks:
            cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

        # Start recording when a face is detected
        if not detection:
            detection = True
            detection_stopped_time = time.time()
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!")

    # Stop recording if no face is detected for a specified time
    if detection:
        if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
            detection = False
            out.release()
            print("Stopped Recording!")

    if detection and out is not None:
        out.write(frame)  # Write the frame to the video file

    cv2.imshow("Camera Feed", frame)

    if cv2.waitKey(1) == ord('q'):
        break

if detection and out is not None:
    out.release()

cap.release()
cv2.destroyAllWindows()