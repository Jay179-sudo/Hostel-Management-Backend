from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command  # NEW
import csv
from django.core.mail import EmailMessage
from io import StringIO
import datetime
import os
from django.utils.dateparse import parse_datetime
from .models import HostelRoom, Student, AbsentAttendance, Hostel, User
import pandas
from django.db.models import F
from .utils import generate_password
from .utils import Util


@shared_task(bind=True)
def process_csv_report(self, start_date=None, end_date=None):
    csvfile = StringIO()
    writer = csv.writer(csvfile)
    # writer.writerow(["Date", "RoomNumber", "Name", "Status"])
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_range = [
        start_date + datetime.timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    ]

    header_row = ["RoomNumber", "Name"]
    header_row.extend(date.strftime("%Y-%m-%d") for date in date_range)
    writer.writerow(header_row)

    # Fetch total students and their attendance for each date
    total_students = HostelRoom.objects.exclude(resident=None).values(
        studentId__email=F("resident__email")
    )

    for student in total_students:
        student_data = [
            HostelRoom.objects.filter(
                resident__email=student["studentId__email"]
            ).values("hostel_room")[0]["hostel_room"],
            Student.objects.filter(user__email=student["studentId__email"]).values(
                "name"
            )[0]["name"],
        ]

        for date in date_range:
            attendance = AbsentAttendance.objects.filter(
                dateAbsent=date, studentId__email=student["studentId__email"]
            ).exists()

            if attendance:
                student_data.append("Absent")
            else:
                student_data.append("Present")

        writer.writerow(student_data)

    email = EmailMessage(
        subject="Attendance CSV",
        body="Attached herewith is your requested CSV File",
        from_email=os.environ.get("EMAIL_FROM"),
        to=["bcs_2021080@iiitm.ac.in"],
    )
    email.attach(
        f"attendance {start_date} to {end_date}.csv",
        csvfile.getvalue(),
        "text/csv",
    )
    email.send()


@shared_task(bind=True)
def create_users(self, url):
    roll_list = pandas.read_csv(url)
    roll_list = roll_list.to_dict(orient="records")
    returnAns = 1
    for data in roll_list:
        user_exists = User.objects.filter(email=data["Email"])
        if user_exists.exists():
            HostelRoom.objects.filter(resident=user_exists[0]).delete()
            user_exists.delete()

        generated_password = generate_password()
        user = User.objects.create_user(
            email=data["Email"], password=generated_password
        )
        user.isStudent = True
        returnAns = user.id
        hostel_occupied = Hostel.objects.get(hostel_code=data["Hostel"])

        student = Student(
            user=user,
            name=data["Name"],
            roll_number=data["Roll"],
            degree_awarded=False,
            Hostel=hostel_occupied,
        )
        hostel_room_exists = HostelRoom.objects.filter(
            Hostel=hostel_occupied, hostel_room=data["Room"]
        ).exists()
        if not hostel_room_exists:
            hostel_room = HostelRoom(
                Hostel=hostel_occupied, hostel_room=data["Room"], resident=user
            )
            hostel_room.save()
        else:
            hostel_room = HostelRoom.objects.get(
                Hostel=hostel_occupied, hostel_room=data["Room"]
            )
            hostel_room.resident = user
            hostel_room.save()
        temp_dict = {
            "subject": "Regarding your student registration account",
            "body": f'Hi! You were recently registered to the Hostel Management Software at ABV-IIITM, Gwalior by your Administrator. Your email is {data["Email"]} and your password is "{generated_password}". Please reach out to the Administration in case of any mistakes.',
            "to_email": data["Email"],
        }
        Util.send_email(temp_dict)
        user.save()
        student.save()

    return returnAns
