# Security-Cameras
A camera system to recognise a human face and take in facial data into a database so that they can be later recognised

## Requirements:

### Installing dlib:

- Go to the official CMake website: cmake.org/download
- Choose the Windows x64 Installer version (e.g., cmake-x.x.x-windows-x86_64.msi).
- Install CMake:

Run the installer.

During installation, choose the option:

- Add CMake to the system PATH (for all users) — this is crucial!

Install Visual Studio (if you don’t have it):

Go to Visual Studio Downloads.
Download and install Visual Studio Community Edition (free version).

Install the Required Components:
During installation, select the "Desktop development with C++" workload.
On the right panel, make sure to check:
Windows 10 SDK
C++ CMake tools for Windows

Restart Your PC (just to be safe).

Open the Developer Command Prompt:
After installation, search for "x64 Native Tools Command Prompt for VS" in the Start menu, and run it.

Try Installing dlib Again:

pip install dlib

## Install other dependencies:
### You also need to install the following Python libraries:
- cv2 (OpenCV): pip install opencv-python
- numpy: pip install numpy
- sqlite3 (comes pre-installed with Python)
### Hardware Requirements:
- A camera must be plugged into the computer for facial detection.

## Directions of use:
tart a new session: Each time you run main.py, ensure that the facial_data.db file is removed (either delete it or move it to another location). This allows the program to create a fresh database to store new facial data.

### Facial detection & recording:
- The program will record 10-second video clips whenever a face is detected in front of the camera.
- A new face is detected when the landmarks are unique (not matching any existing face in the database).
- The facial data (landmarks) will be recorded into the database. These data are stored with timestamps and the face's unique face_id.
- The face is checked against the existing database using a tolerance value (found inside the is_face_in_database function). - Increasing the tolerance allows the program to recognize the face even with variations in facial landmarks.
### Tolerance setting:
- The tolerance is the threshold for how much change in facial landmarks is allowed before the system considers it a new face.
- You can modify this tolerance by adjusting the value in the is_face_in_database function.
### Recording videos:
- The program starts recording a video when a face is detected, and it stops recording if no face is detected for a specified time (default is 10 seconds).
- Each video is saved with a timestamp.
