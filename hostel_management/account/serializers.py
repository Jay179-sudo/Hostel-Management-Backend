from rest_framework import serializers
from account.models import (
    User,
    SuperAdmin,
    HostelAdmin,
    Hostel,
    MessManager,
    Student,
    LeaveRequest,
    AbsentAttendance,
    HostelRoom,
    AbsentAttendance,
)
from .utils import Util, trial
from django.utils.dateparse import parse_datetime
from datetime import datetime


# send password reset emails
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .tasks import create_users


class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.isSuperAdmin = True
        superAdmin = SuperAdmin(user=user)
        superAdmin.save()
        user.save()
        return user


class SuperAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = "__all__"


class HostelAdminSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    hostel_supervised = serializers.CharField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        hostel_supervised_id = validated_data.pop("hostel_supervised")
        user = User.objects.create_user(**validated_data)
        user.isHostelAdmin = True
        hostel_supervised = Hostel.objects.get(hostel_code=hostel_supervised_id)
        hostelAdmin = HostelAdmin(user=user, hostel_supervised=hostel_supervised)
        hostelAdmin.save()
        user.save()
        return user


class HostelAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


class MessManagerSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    hostel_catered = serializers.CharField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        hostel_supervised_id = validated_data.pop("hostel_catered")
        user = User.objects.create_user(**validated_data)
        user.isMessManager = True
        hostel_supervised = Hostel.objects.get(hostel_code=hostel_supervised_id)
        hostelAdmin = MessManager(user=user, hostel_catered=hostel_supervised)
        hostelAdmin.save()
        user.save()
        return user


class MessManagerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


class StudentSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    name = serializers.CharField(max_length=100)
    Roll_Number = serializers.CharField(max_length=50)
    Hostel = serializers.CharField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        hostel_supervised_id = validated_data.pop("Hostel")
        name = validated_data.pop("name")
        roll_number = validated_data.pop("Roll_Number")

        user = User.objects.create_user(**validated_data)
        user.isStudent = True
        user.save()
        hostel_supervised = Hostel.objects.get(hostel_code=hostel_supervised_id)

        student = Student(
            user=user,
            name=name,
            roll_number=roll_number,
            degree_awarded=False,
            Hostel=hostel_supervised,
        )
        student.save()

        return user


class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()

    def validate(self, attrs):
        return attrs


# Pachi gayera overriden this one
class LeaveSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    Address = serializers.CharField(max_length=100)
    AdminApproved = serializers.BooleanField(default=False)
    ReasonForLeave = serializers.CharField(max_length=100)
    hostel = serializers.IntegerField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        start_date = validated_data.pop("start_date")
        end_date = validated_data.pop("end_date")
        Address = validated_data.pop("Address")
        ReasonForLeave = validated_data.pop("ReasonForLeave")
        hostel = validated_data.pop("hostel")

        user = User.objects.get(email=email, password=password)
        student = Student.objects.get(user=user)
        hostel = Hostel.objects.get(pk=hostel)
        Leave = LeaveRequest(
            student=student,
            start_date=start_date,
            end_date=end_date,
            Address=Address,
            AdminApproved="PENDING",
            EmailSent=False,
            ReasonForLeave=ReasonForLeave,
            hostel=hostel,
        )
        Leave.save()

        return user


# User Profile Serializer


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]


# Change password


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    # old password
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    # new password

    def validate(self, attrs):
        email = self.context.get("user_email")
        user_req = self.context.get("user_request")
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = User.objects.get(email=email)
        success = user.check_password(raw_password=password)
        if success:
            user.set_password(password2)
            user.save()
            return attrs
        else:
            raise serializers.ValidationError("Password does not match")


# Password Reset Emails


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            link = "http://localhost:3000/api/user/reset/" + uid + "/" + token

            # send email
            body = "Click the following link to reset your password " + link
            # data variable ma subject, body, ... diney
            data = {
                "subject": "Rest Your Password",
                "body": body,
                "to_email": user.email,
            }
            Util.send_email(data)

            return attrs
        else:
            raise serializers.ValidationError("You are not a registered user!")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    def validate(self, attrs):
        try:
            user_req = self.context.get("user_request")
            password = attrs.get("password")

            uid = self.context.get("uid")
            token = self.context.get("token")

            # id nikalam user ko
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)

            # aaba token check garne. Token thik cha ki nai check garnu paryo
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    "Access Denied! Invalid or expired token"
                )

            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Access Denied! Invalid or expired token")


class CreateLeaveRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    Address = serializers.CharField(max_length=100)
    ReasonForLeave = serializers.CharField(max_length=100)

    def validate(self, attrs):
        start = datetime.strptime(attrs.get("start_date"), "%Y-%m-%d").date()
        end = datetime.strptime(attrs.get("end_date"), "%Y-%m-%d").date()

        if start > end:
            raise serializers.ValidationError(
                "Start date and End Date is not consistent"
            )
        else:
            return attrs

    def create(self, validated_data):
        email = validated_data.get("email")
        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")
        Address = validated_data.get("Address")
        ReasonForLeave = validated_data.get("ReasonForLeave")

        user = User.objects.get(email=email)
        hostel = Student.objects.get(user=user)
        if LeaveRequest.objects.filter(
            student=user, start_date=start_date, end_date=end_date
        ):
            raise serializers.ValidationError("Cannot store duplicate data")
        LeaveReq = LeaveRequest(
            student=user,
            hostel=hostel.Hostel,
            start_date=start_date,
            end_date=end_date,
            Address=Address,
            ReasonForLeave=ReasonForLeave,
            EmailSent=False,
        )
        LeaveReq.save()

        return LeaveReq


class ReadLeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            "start_date",
            "end_date",
            "Address",
            "AdminApproved",
            "ReasonForLeave",
        ]

    def validate(self, attrs):
        return attrs


class UpdateHostelRoomAllocation(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    room = serializers.CharField(max_length=10)

    def validate(self, attrs):
        user = User.objects.get(email=self.initial_data["email"]).id
        hostelRoom = HostelRoom.objects.get(resident=user)
        hostelRoom.hostel_room = attrs.get("room")
        hostelRoom.save()
        return attrs


class CreateHostelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=100)
    hostel_code = serializers.CharField(max_length=5)
    capacity = serializers.IntegerField()

    def validate(self, attrs):
        # check if hostel having the same code has not been created already
        return attrs

    def create(self, validated_data):
        hostelObj = Hostel(
            name=validated_data.get("name"),
            location=validated_data.get("location"),
            hostel_code=validated_data.get("hostel_code"),
            capacity=validated_data.get("capacity"),
        )
        hostelObj.save()

        return hostelObj


class CreateHostelAdminSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    # expect the hostel code
    hostel_supervised = serializers.CharField()

    def validate(self, attrs):
        # check if hostel exists or not
        return attrs

    def create(self, validated_data):
        hostel_supervised = validated_data.pop("hostel_supervised")
        user = User.objects.create_user(**validated_data)
        hostel = Hostel.objects.get(hostel_code=hostel_supervised)
        hostelAdmin = HostelAdmin(user=user, hostel_supervised=hostel)
        hostelAdmin.save()
        return hostelAdmin


class CreateMessManagerSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    # expect the hostel code
    hostel_supervised = serializers.CharField()

    def validate(self, attrs):
        # check if hostel exists or not
        return attrs

    def create(self, validated_data):
        hostel_supervised = validated_data.pop("hostel_supervised")
        user = User.objects.create_user(**validated_data)
        hostel = Hostel.objects.get(hostel_code=hostel_supervised)
        hostelMess = MessManager(user=user, hostel_catered=hostel)
        hostelMess.save()
        return hostelMess


class CreateStudentSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)
    # expect the hostel code
    hostel = serializers.CharField()
    name = serializers.CharField(max_length=100)
    roll_number = serializers.CharField(max_length=50)

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        hostel_char = validated_data.pop("hostel")
        name = validated_data.pop("name")
        roll_number = validated_data.pop("roll_number")

        user = User.objects.create(**validated_data)
        hostel = Hostel.objects.get(hostel_code=hostel_char)
        student = Student(
            user=user,
            Hostel=hostel,
            name=name,
            roll_number=roll_number,
            degree_awarded=False,
            Room_Number=-1,
        )
        student.save()
        return student


class ListStudentsHostelToday(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["roll_number", "name"]


# ________________________NEW UPDATES__________________________________


class csvSerializer(serializers.Serializer):
    csv = serializers.CharField()


    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        try:
            sheet_url = validated_data.get("csv")
            url = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            create_users.delay(url)
            return User.objects.filter(id__gte=1)[0]
        except:
            raise serializers.ValidationError("Please provide correct format of link")


class viewStudentsPresentYesterdaySerializer(serializers.Serializer):
    number = serializers.IntegerField()


class daterangeStudentListSerializer(serializers.Serializer):
    start_date = serializers.CharField()
    end_date = serializers.CharField()


class daterangeSpecificStudentListSerializer(serializers.Serializer):
    dateAbsent = serializers.DateField()


class AbsentAttendanceSerializer(serializers.Serializer):
    studentId__email = serializers.EmailField()
    num_days = serializers.IntegerField()


class AbsentTodaySerializer(serializers.Serializer):
    hostel_room = serializers.IntegerField()


class updateabsentSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        email = validated_data.get("email")
        user = User.objects.get(email=email)

        absentuser = AbsentAttendance(studentId=user)
        absentuser.save()

        return user


# last update
class deletefromRoomSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        try:
            email = validated_data("email")
            user = User.objects.get(email=email)
            hostel_room = HostelRoom.objects.get(resident=user)
            hostel_room.hostel_room = -1
        except:
            raise serializers.ValidationError("Multiple students present in room!")
        return user


class getEmailFromRoomSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        return attrs


class getRoomDetailsSerializer(serializers.Serializer):
    hostel_room = serializers.IntegerField()
    Hostel__hostel_code = serializers.CharField()
    resident__email = serializers.EmailField()

    def validate(self, attrs):
        return attrs


class occupiedRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelRoom
        fields = "__all__"


class listLeaveRequestsSerializer(serializers.Serializer):
    start_date = serializers.CharField()
    end_date = serializers.CharField()
    student__email = serializers.CharField()
    hostel__name = serializers.CharField()


class AbsentCSV(serializers.Serializer):
    Date = serializers.DateField()
    RoomNumber = serializers.IntegerField()
    Name = serializers.CharField()
    Status = serializers.CharField()
