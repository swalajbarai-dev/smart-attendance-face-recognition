import os
from datetime import datetime
import pandas as pd


def mark_attendance(
    student_name,
    subject,
    attendance_file="data/attendance/attendance.csv"
):
    """
    Mark attendance for a student.

    A student can give attendance only once per day,
    regardless of the subject.

    Returns:
        True  -> attendance recorded successfully
        False -> attendance already recorded today
    """

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    os.makedirs(
        os.path.dirname(attendance_file),
        exist_ok=True
    )

    # Load existing attendance
    if os.path.exists(attendance_file):

        df = pd.read_csv(attendance_file)

    else:

        df = pd.DataFrame(
            columns=[
                "Name",
                "Subject",
                "Date",
                "Time",
                "Status"
            ]
        )

    # Make sure required columns exist
    if "Subject" not in df.columns:
        df["Subject"] = "Unknown"

    # -----------------------------------------
    # IMPORTANT:
    # Check ONLY student name + today's date
    # -----------------------------------------

    already_marked = (
        (df["Name"].astype(str).str.strip().str.lower()
         == student_name.strip().lower()) &
        (df["Date"].astype(str) == today)
    ).any()

    if already_marked:

        return False

    # -----------------------------------------
    # Attendance has not been recorded today
    # -----------------------------------------

    new_record = pd.DataFrame(
        [{
            "Name": student_name,
            "Subject": subject,
            "Date": today,
            "Time": current_time,
            "Status": "Present"
        }]
    )

    df = pd.concat(
        [df, new_record],
        ignore_index=True
    )

    df = df[
        [
            "Name",
            "Subject",
            "Date",
            "Time",
            "Status"
        ]
    ]

    df.to_csv(
        attendance_file,
        index=False
    )

    return True
