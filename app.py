import cv2
import face_recognition
import time

from src.face_recognition import load_known_faces
from src.attendance import mark_attendance
from src.notifications import send_attendance_notifications


KNOWN_FACES_DIR = "data/known_faces"
ATTENDANCE_FILE = "data/attendance/attendance.csv"

MATCH_THRESHOLD = 0.5

# Wait 2 seconds after recognition
MESSAGE_DELAY = 2

# Keep webcam message visible for 5 seconds
MESSAGE_DURATION = 5


def main():

    print("Loading registered faces...")

    known_encodings, known_names = load_known_faces(
        KNOWN_FACES_DIR
    )

    print(
        f"Loaded {len(known_names)} registered face(s)."
    )

    if not known_encodings:
        print("No registered faces found.")
        return

    print("Starting camera...")
    print("Press Q to quit.")

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Could not open webcam.")
        return

    # ------------------------------------------------
    # VARIABLES
    # ------------------------------------------------

    # Keeps track of people already processed
    # during THIS webcam run.
    processed_this_run = set()

    # Message shown on webcam
    attendance_message = ""

    # When face was recognized
    recognition_time = 0

    # When message started displaying
    message_start_time = 0

    # Are we waiting for the 2-second delay?
    waiting_for_message = False

    # Student who should receive notification
    pending_notification_student = None

    # Prevent duplicate SMS/call
    notification_sent = False

    # ------------------------------------------------
    # CAMERA LOOP
    # ------------------------------------------------

    while True:

        success, frame = camera.read()

        if not success:
            print("Could not read frame.")
            break

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        face_locations = face_recognition.face_locations(
            rgb_frame
        )

        face_encodings = face_recognition.face_encodings(
            rgb_frame,
            face_locations
        )

        recognized_count = 0
        unknown_count = 0

        current_time = time.time()

        # ------------------------------------------------
        # FACE RECOGNITION
        # ------------------------------------------------

        for face_location, face_encoding in zip(
            face_locations,
            face_encodings
        ):

            name = "Unknown"
            match_score = 0

            face_distances = face_recognition.face_distance(
                known_encodings,
                face_encoding
            )

            if len(face_distances) > 0:

                best_match_index = face_distances.argmin()

                best_distance = face_distances[
                    best_match_index
                ]

                match_score = max(
                    0,
                    min(
                        100,
                        (1 - best_distance) * 100
                    )
                )

                # ----------------------------------------
                # FACE MATCHED
                # ----------------------------------------

                if best_distance < MATCH_THRESHOLD:

                    name = known_names[
                        best_match_index
                    ]

                    recognized_count += 1

                    # ------------------------------------
                    # ONLY PROCESS NEW PERSON IN THIS RUN
                    # ------------------------------------

                    if name not in processed_this_run:

                        processed_this_run.add(name)

                        # --------------------------------
                        # CHECK / SAVE ATTENDANCE
                        # --------------------------------

                        marked = mark_attendance(
                            name,
                            "Computer Vision",
                            ATTENDANCE_FILE
                        )

                        # Start 2-second timer
                        recognition_time = current_time
                        waiting_for_message = True

                        # --------------------------------
                        # NEW ATTENDANCE
                        # --------------------------------

                        if marked:

                            attendance_message = (
                                "Attendance recorded successfully"
                            )

                            # Save student for notification
                            pending_notification_student = name

                            notification_sent = False

                            print()
                            print(
                                f"New attendance recorded: {name}"
                            )
                            print(
                                "Waiting 2 seconds..."
                            )

                        # --------------------------------
                        # DUPLICATE ATTENDANCE
                        # --------------------------------

                        else:

                            attendance_message = (
                                "Can't give attendance twice"
                            )

                            # VERY IMPORTANT:
                            # No notification for duplicate
                            pending_notification_student = None

                            notification_sent = False

                            print()
                            print(
                                f"Attendance already exists: {name}"
                            )
                            print(
                                "No SMS or call will be sent."
                            )

                else:

                    unknown_count += 1

            # ------------------------------------------------
            # DRAW FACE BOX
            # ------------------------------------------------

            top, right, bottom, left = face_location

            if name != "Unknown":

                box_color = (0, 255, 0)

                label = (
                    f"{name} | Match: "
                    f"{match_score:.1f}%"
                )

            else:

                box_color = (0, 0, 255)

                label = (
                    f"Unknown | Match: "
                    f"{match_score:.1f}%"
                )

            cv2.rectangle(
                frame,
                (left, top),
                (right, bottom),
                box_color,
                2
            )

            label_height = 35

            cv2.rectangle(
                frame,
                (left, bottom - label_height),
                (right, bottom),
                box_color,
                cv2.FILLED
            )

            cv2.putText(
                frame,
                label,
                (left + 6, bottom - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

        # ------------------------------------------------
        # WAIT 2 SECONDS
        # ------------------------------------------------

        if (
            waiting_for_message
            and current_time - recognition_time
            >= MESSAGE_DELAY
        ):

            # Message starts now
            message_start_time = current_time

            waiting_for_message = False

            # --------------------------------------------
            # SEND SMS + CALL ONLY FOR NEW ATTENDANCE
            # --------------------------------------------

            if (
                pending_notification_student
                and not notification_sent
            ):

                print()
                print(
                    "2 seconds completed."
                )

                print(
                    "Showing attendance message."
                )

                print(
                    "Sending SMS and call..."
                )

                send_attendance_notifications(
                    pending_notification_student
                )

                notification_sent = True

                pending_notification_student = None

        # ------------------------------------------------
        # SHOW MESSAGE FOR 5 SECONDS
        # ------------------------------------------------

        if (
            attendance_message
            and message_start_time > 0
            and current_time - message_start_time
            < MESSAGE_DURATION
        ):

            box_left = 50
            box_top = 120
            box_right = frame.shape[1] - 50
            box_bottom = 190

            cv2.rectangle(
                frame,
                (box_left, box_top),
                (box_right, box_bottom),
                (255, 255, 255),
                cv2.FILLED
            )

            text_size = cv2.getTextSize(
                attendance_message,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                2
            )[0]

            text_x = (
                frame.shape[1] - text_size[0]
            ) // 2

            text_y = 165

            cv2.putText(
                frame,
                attendance_message,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 0),
                2
            )

        # ------------------------------------------------
        # CAMERA INFORMATION
        # ------------------------------------------------

        cv2.putText(
            frame,
            f"Recognized: {recognized_count}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"Unknown: {unknown_count}",
            (20, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Press Q to quit",
            (20, 95),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Smart Attendance System",
            frame
        )

        # ------------------------------------------------
        # Q = STOP CAMERA
        # ------------------------------------------------

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # ------------------------------------------------
    # CLOSE CAMERA
    # ------------------------------------------------

    camera.release()

    cv2.destroyAllWindows()

    print()
    print("Webcam stopped.")
    print("Attendance data saved in CSV.")


if __name__ == "__main__":
    main()