import os
import cv2
import face_recognition


def load_known_faces(known_faces_dir):
    """
    Load student images and generate face encodings.

    Directory structure:

    known_faces/
        Rahul/
            photo1.jpg
        Priya/
            photo1.jpg

    Returns:
        known_encodings
        known_names
    """

    known_encodings = []
    known_names = []

    for student_name in os.listdir(known_faces_dir):

        student_path = os.path.join(
            known_faces_dir,
            student_name
        )

        if not os.path.isdir(student_path):
            continue

        for image_name in os.listdir(student_path):

            image_path = os.path.join(
                student_path,
                image_name
            )

            image = cv2.imread(image_path)

            if image is None:
                continue

            rgb_image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2RGB
            )

            face_locations = face_recognition.face_locations(
                rgb_image
            )

            if not face_locations:
                print(
                    f"No face found in: {image_path}"
                )
                continue

            encodings = face_recognition.face_encodings(
                rgb_image,
                face_locations
            )

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(student_name)

    return known_encodings, known_names


def recognize_face(
    face_image,
    known_encodings,
    known_names
):
    """
    Recognize a face from a camera frame.

    Returns:
        Student name or 'Unknown'
    """

    rgb_image = cv2.cvtColor(
        face_image,
        cv2.COLOR_BGR2RGB
    )

    face_locations = face_recognition.face_locations(
        rgb_image
    )

    if not face_locations:
        return "Unknown"

    face_encodings = face_recognition.face_encodings(
        rgb_image,
        face_locations
    )

    if not face_encodings:
        return "Unknown"

    current_encoding = face_encodings[0]

    matches = face_recognition.compare_faces(
        known_encodings,
        current_encoding,
        tolerance=0.5
    )

    if True in matches:

        first_match_index = matches.index(True)

        return known_names[first_match_index]

    return "Unknown"