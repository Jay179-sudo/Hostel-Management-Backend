# email lai ho yo. Password reset

from django.core.mail import EmailMessage
import os
from .models import Student, User, Hostel, HostelRoom


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=os.environ.get("EMAIL_FROM"),
            to=[data["to_email"]],
        )

        email.send()


import pandas
import random


def generate_password():
    letters = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    return password


def trial(url):
    # url = "https://drive.google.com/file/d/121Yzy3iJ_LyOoUDLcz8OlNsvVrqrxba_/view"
    # url = "https://drive.google.com/uc?id=" + url.split("/")[-2]
    # goes in the view or serializer logic
    print(url)
    roll_list = pandas.read_csv(url)
    print("go")
    roll_list = roll_list.to_dict(orient="records")
    returnAns = 1
    print(roll_list)
    for data in roll_list:
        user_exists = User.objects.filter(email=data["Email"]).exists()
        print("This ", user_exists)
        if not user_exists:
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
            temp_dict = {
                "subject": "Regarding your student registration account",
                "body": f'Your email is {data["Email"]} and your password is {generated_password}',
                "to_email": data["Email"],
            }
            # Util.send_email(temp_dict)
            user.save()
            student.save()

    return returnAns
