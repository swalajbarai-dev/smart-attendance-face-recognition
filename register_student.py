import os
import cv2
import face_recognition


KNOWN_FACES_DIR = "data/known_faces"

TOTAL_PHOTOS = 3


def register_student():

    student_name = input(
        "Enter student name: "
    ).strip()

    if not student_name:
        print("Student name cannot be empty.")
        return

    student_folder = os.path.join(
        KNOWN_FACES_DIR,
        student_name
    )

    os.makedirs(
        student_folder,
        exist_ok=True
    )

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open webcam.")
        return

    print()
    print("Camera started.")
    print()
    print("We will capture 3 photos.")
    print("Change your position slightly for each photo.")
    print("Press SPACE to capture.")
    print("Press Q to cancel.")
    print()

    photo_count = 0

    while True:

        success, frame = camera.read()

        if not success:
            print("Could not read camera frame.")
            break

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(
            rgb_frame
        )

        # Draw face rectangles
        for face_location in face_locations:

            top, right, bottom, left = face_location

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                (0, 255, 0),
                2
            )

        # Display progress
        cv2.putText(
            frame,
            f"Photos: {photo_count}/{TOTAL_PHOTOS}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "SPACE = Capture | Q = Quit",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Student Registration",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # Capture photo
        if key == ord(" "):

            if len(face_locations) == 0:

                print(
                    "No face detected. "
                    "Please look at the camera."
                )

                continue

            if len(face_locations) > 1:

                print(
                    "Multiple faces detected. "
                    "Only one person should be visible."
                )

                continue

            # Generate encoding to verify face
            encodings = face_recognition.face_encodings(
                rgb_frame,
                face_locations
            )

            if not encodings:

                print(
                    "Could not generate face encoding."
                )

                continue

            photo_count += 1

            photo_path = os.path.join(
                student_folder,
                f"photo{photo_count}.jpg"
            )

            cv2.imwrite(
                photo_path,
                frame
            )

            print(
                f"Photo {photo_count}/{TOTAL_PHOTOS} saved."
            )

            # Change position for next photo
            if photo_count == 1:

                print(
                    "Good! Now turn your face slightly LEFT."
                )

            elif photo_count == 2:

                print(
                    "Good! Now turn your face slightly RIGHT."
                )

            elif photo_count == 3:

                print()
                print(
                    f"Student '{student_name}' "
                    "registered successfully!"
                )

                break

        # Cancel
        elif key == ord("q"):

            print("Registration cancelled.")
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    register_student()