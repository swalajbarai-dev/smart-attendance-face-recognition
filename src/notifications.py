import os
import json

from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

STUDENTS_FILE = "data/students.json"


def get_student_phone(student_name):

    if not os.path.exists(STUDENTS_FILE):
        print("students.json not found.")
        return None

    with open(STUDENTS_FILE, "r") as file:
        students = json.load(file)

    return students.get(student_name)


def send_attendance_sms(student_name, phone_number):

    client = Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN
    )

    message = client.messages.create(
        body="sms_event_notifications",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    print(f"Trial SMS sent to {student_name}")
    print(f"SMS SID: {message.sid}")

    return True


def send_attendance_call(student_name, phone_number):

    client = Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN
    )

    # Trial Voice request
    call = client.calls.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        url="https://webhooks.twilio.com/v1/Voice/Template/voice_text_to_speech"
    )

    print(f"Trial call started for {student_name}")
    print(f"Call SID: {call.sid}")

    return True


def send_attendance_notifications(student_name):

    phone_number = get_student_phone(student_name)

    if not phone_number:
        print(
            f"No phone number found for {student_name}"
        )
        return False

    print()
    print(
        f"Sending notifications to {student_name}..."
    )

    sms_success = False
    call_success = False

    # SMS
    try:

        sms_success = send_attendance_sms(
            student_name,
            phone_number
        )

    except Exception as e:

        print("SMS failed:")
        print(e)

    # CALL
    try:

        call_success = send_attendance_call(
            student_name,
            phone_number
        )

    except Exception as e:

        print("Call failed:")
        print(e)

    return sms_success or call_success