# Smart Attendance using Face Recognition

A simple computer vision based attendance system that uses face recognition to identify students and automatically record their attendance in a CSV file.

The project uses a webcam to detect and recognize registered students. When a student is recognized, the system checks whether attendance has already been recorded for that day.

## Features

- Webcam-based face detection
- Face recognition using `face_recognition`
- Register new students using webcam photos
- Stores multiple photos for each student
- Automatic attendance marking
- Prevents duplicate attendance on the same day
- Shows recognition confidence/match percentage
- Displays attendance messages on the webcam
- Stores attendance in a CSV file
- SMS and voice call notification using Twilio
- Uses Twilio trial features without requiring an upgrade

## Technologies Used

- Python
- OpenCV
- Face Recognition
- NumPy
- Pandas
- Twilio
- Python-dotenv

## Project Structure

```text
smart-attendance-face-recognition/
│
├── app.py
├── register_student.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── known_faces/
│   │   ├── Abhradwip/
│   │   ├── dwaj/
│   │   └── swalaj/
│   │
│   ├── attendance/
│   │   └── attendance.csv
│   │
│   └── students.json
│
├── src/
│   ├── __init__.py
│   ├── face_detection.py
│   ├── face_recognition.py
│   ├── attendance.py
│   └── notifications.py
│
└── models/