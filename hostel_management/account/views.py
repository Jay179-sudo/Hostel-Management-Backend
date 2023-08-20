from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .serializers import (
    SuperAdminSerializer,
    HostelAdminSerializer,
    HostelSerializer,
    MessManagerSerializer,
    SuperAdminLoginSerializer,
    StudentSerializer,
    LeaveSerializer,
    StudentLoginSerializer,
    HostelAdminLoginSerializer,
    MessManagerLoginSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    SendPasswordResetEmailSerializer,
    UserPasswordResetSerializer,
    # student serializer view
    CreateLeaveRequestSerializer,
    ReadLeaveRequestSerializer,
    # Hostel Admin
    UpdateHostelRoomAllocation,
    # Super Admin
    # Mess Manager
    ListStudentsHostelToday,
    # new update
    csvSerializer,
    viewStudentsPresentYesterdaySerializer,
    daterangeStudentListSerializer,
    updateabsentSerializer,
    AbsentAttendanceSerializer,
    getEmailFromRoomSerializer,
    deletefromRoomSerializer,
    getRoomDetailsSerializer,
    occupiedRoomSerializer,
    daterangeSpecificStudentListSerializer,
    AbsentTodaySerializer,
    listLeaveRequestsSerializer,
    AbsentCSV,
)
import os
from .models import (
    Student,
    LeaveRequest,
    MessManager,
    SuperAdmin,
    HostelAdmin,
    Hostel,
    HostelRoom,
    AbsentAttendance,
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from .permissions import StudentOnly, MessManagerOnly, HostelAdminOnly, SuperAdminOnly
import datetime
import jwt
import csv
from django.core.mail import EmailMessage
from io import StringIO
from .tasks import process_csv_report


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class SuperAdminRegister(APIView):
    serializer_class = SuperAdminSerializer

    def post(self, request, format=None):
        serializer = SuperAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration successful!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class HostelAdminRegister(APIView):
    serializer_class = HostelAdminSerializer

    def post(self, request, format=None):
        serializer = HostelAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Hostel Admin registered!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class HostelRegister(APIView):
    serializer_class = HostelSerializer

    def post(self, request, format=None):
        serializer = HostelSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Hostel registered!"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class MessManagerRegister(APIView):
    serializer_class = MessManagerSerializer

    def post(self, request, format=None):
        serializer = MessManagerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Hostel registered!"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class StudentRegister(APIView):
    serializer_class = StudentSerializer

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Student Registration successful!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


class LeaveRegister(APIView):
    serializer_class = LeaveSerializer

    def post(self, request, format=None):
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"msg": "Leave Request registered!"}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"msg": "Registration unsuccessful"}, status=status.HTTP_400_BAD_REQUEST
        )


# Login View


class SuperAdminLoginView(APIView):
    def post(self, request, format=None):
        serializer = SuperAdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login successful!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class HostelAdminLogin(APIView):
    def post(self, request, format=None):
        serializer = HostelAdminLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login successful!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class MessManagerLogin(APIView):
    def post(self, request, format=None):
        serializer = MessManagerLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login successful!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class StudentLogin(APIView):
    def post(self, request, format=None):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login successful!"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors": ["Email or password is not Valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


# Profile View


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Change password


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    # is authetnicated bhaneko token pathau header ma
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data,
            context={"user_email": request.user.email, "user_request": request.user},
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Change Successful!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmail(APIView):
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Reset link sent. Please check your Email"},
                status=status.HTTP_200_OK,
            )
        # raise exception garey bhane no need to send a failure response, but failure response malai better way laagyo ngl


# yo maathi ko change garna lai


class UserPasswordResetView(APIView):
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data,
            context={"uid": uid, "token": token, "user_req": self.request.user},
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"msg": "Password Reset successful!"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # id chai user lai identify garna whereas token chai kei hawa request ta aako chaina ni confirm garira.


class CreateReadLeaveRequestsStudent(APIView):
    # permission_classes = [StudentOnly]

    def post(self, request, format=None):
        leaveSerializer = CreateLeaveRequestSerializer(data=request.data)
        try:
            if leaveSerializer.is_valid():
                leaveSerializer.save()
                return Response(
                    {"msg": "Leave Request Created"}, status=status.HTTP_201_CREATED
                )
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, request, format=None):
        try:
            user = User.objects.get(email=request.data["email"])
            LeaveObj = LeaveRequest.objects.get(student=user)
            LeaveSerializer = ReadLeaveRequestSerializer(data=LeaveObj.__dict__)
            if LeaveSerializer.is_valid():
                return Response(LeaveSerializer.data)
            return Response(
                LeaveSerializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UpdateRoomAllocation(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UpdateHostelRoomAllocation(data=request.data)
        if serializer.is_valid():
            return Response({"msg": "Room Updated!"}, status=status.HTTP_202_ACCEPTED)
        return Response(
            {"msg": "Request Failed. Please try again later!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListStudentsPresentView(ListAPIView):
    # permission_classes = [MessManager]
    serializer_class = ListStudentsHostelToday

    def get_queryset(self):
        user = self.request.user
        hostel = MessManager.objects.filter(user=user).hostel_catered
        return Student.objects.filter(Hostel=hostel)


# _________________________NEW UPDATE______________________________


class UploadCSV(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            serializer = csvSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Students Created!"}, status=status.HTTP_202_ACCEPTED
                )
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ok
class viewStudentsPresentYesterday(APIView):
    # permission_classes = [MessManagerOnly]

    def get(self, request, format=None):
        occupied = hostelRoom = HostelRoom.objects.exclude(hostel_room=None)
        date_today = datetime.date.today()
        date_yesterday = date_today - datetime.timedelta(days=1)
        try:
            students = AbsentAttendance.objects.filter(dateAbsent=date_yesterday)

            if students.exists():
                return Response(
                    {"number": len(students), "total_occupied": len(occupied)},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"number": 0, "total_occupied": len(occupied)},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# chat
from django.db.models import Count


class AbsentDaysSpecificView(APIView):
    # permission_classes = [HostelAdminOnly]

    def post(self, request):
        email = request.data.get("email")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        if not start_date or not end_date:
            return Response(
                {"error": "Please provide both start_date and end_date."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email=email).id
            absent_days = AbsentAttendance.objects.filter(
                dateAbsent__range=[start_date, end_date], studentId=user
            ).values("dateAbsent")
            serializer = daterangeSpecificStudentListSerializer(absent_days, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"error": "Please provide both start_date and end_date."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# ok
class AbsentDaysView(APIView):
    def post(self, request):
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        try:
            if not start_date or not end_date:
                return Response(
                    {"error": "Please provide both start_date and end_date."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            absent_days = (
                AbsentAttendance.objects.filter(
                    dateAbsent__range=[start_date, end_date]
                )
                .values("studentId__email")
                .annotate(num_days=Count("dateAbsent"))
            )

            serializer = AbsentAttendanceSerializer(absent_days, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# checking absent record
class checkAbsentRecord(APIView):
    def post(self, request, format=None):
        try:
            email = request.data["email"]
            dateAbsent = datetime.date.today()
            absent_record = AbsentAttendance.objects.filter(
                studentId__email=email, dateAbsent=dateAbsent
            )
            if absent_record.exists():
                return Response(
                    {"msg": "Absent"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"msg": "Present"},
                    status=status.HTTP_200_OK,
                )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# creating absent record
class createabsentrecord(APIView):
    # permission_classes = [HostelAdminOnly]

    def post(self, request, format=None):
        try:
            serializer = updateabsentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"msg": "Absentee Recorded!"}, status=status.HTTP_202_ACCEPTED
                )
            else:
                return Response(
                    {"msg": "Request Failed. Please try again later!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class deleteAbsent(APIView):
    def post(self, request, format=None):
        try:
            email = request.data["email"]
            dateAbsent = datetime.date.today()
            absent_record = AbsentAttendance.objects.get(
                studentId__email=email, dateAbsent=dateAbsent
            )
            absent_record.delete()
            return Response(
                {"msg": "Successful!"},
                status=status.HTTP_202_ACCEPTED,
            )

        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# checking if absent today
class AbsentToday(APIView):
    def get(self, request):
        try:
            absent_people = AbsentAttendance.objects.filter(
                dateAbsent=datetime.date.today()
            ).values("studentId")
            student_ids = [item["studentId"] for item in absent_people]
            room_absent = HostelRoom.objects.filter(resident__in=student_ids).values(
                "hostel_room"
            )
            serializer = AbsentTodaySerializer(room_absent, many=True)
            return Response(serializer.data)
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# delete student from room
class deletefromRoom(APIView):
    def post(self, request):
        serializer = deletefromRoomSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"msg": "Room allocation cleared!"}, status=status.HTTP_202_ACCEPTED
                )
            except:
                return Response(
                    {"msg": "Request Failed. Please try again later!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {"msg": "Request Failed. Please try again later!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# get email of resident from room number
class getRoomFromEmail(APIView):
    def post(self, request):
        room_number = request.data.get("room_number")
        try:
            hostel_room = HostelRoom.objects.get(hostel_room=room_number)
        except ObjectDoesNotExist:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if hostel_room.resident:
            serializer = getEmailFromRoomSerializer(hostel_room.resident)
            return Response(serializer.data)


# get room details from room number
class getRoomDetails(APIView):
    def post(self, request):
        try:
            room_number = request.data.get("room_number")
            hostelRoom = HostelRoom.objects.filter(hostel_room=room_number).values(
                "hostel_room", "Hostel__hostel_code", "resident__email"
            )

            if hostelRoom:
                serializer = getRoomDetailsSerializer(hostelRoom[0])
                return Response(serializer.data)
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


# list of rooms that are occupied
class unoccupiedRooms(APIView):
    def get(self, request, format=None):
        hostelRoom = HostelRoom.objects.filter(hostel_room=None)

        serializer = occupiedRoomSerializer(hostelRoom, many=True)
        return Response(serializer.data)


# list of rooms that are unoccupied
class occupiedRooms(APIView):
    def get(self, request, format=None):
        hostelRoom = HostelRoom.objects.exclude(resident=None)

        serializer = occupiedRoomSerializer(hostelRoom, many=True)
        return Response(serializer.data)


# list of leave requests
class listLeaveRequests(APIView):
    def post(self, request, format=None):
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        leaverequests = LeaveRequest.objects.filter(
            start_date__gte=start_date, end_date__lte=end_date
        ).values(
            "start_date",
            "end_date",
            "student__email",
            "hostel__name",
        )

        serializer = listLeaveRequestsSerializer(leaverequests, many=True)

        return Response(serializer.data)


class getsUserType(APIView):
    def post(self, request, format=None):
        try:
            token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
            trial = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms="HS256")
            user = User.objects.get(id=trial["user_id"])

            if user.isSuperAdmin:
                return Response(
                    {"msg": "SUPER ADMIN"},
                    status=status.HTTP_200_OK,
                )
            elif user.isHostelAdmin:
                return Response(
                    {"msg": "HOSTEL ADMIN"},
                    status=status.HTTP_200_OK,
                )
            elif user.isMessManager:
                return Response(
                    {"msg": "MESS MANAGER"},
                    status=status.HTTP_200_OK,
                )
            elif user.isStudent:
                return Response(
                    {"msg": "STUDENT"},
                    status=status.HTTP_200_OK,
                )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


from django.db.models import F


class GetAttendanceCSVViewSet(APIView):
    def post(self, request):
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")

        try:
            process_csv_report.delay(start_date=start_date, end_date=end_date)
            return Response(
                {"msg": "Request Successful!"},
                status=status.HTTP_200_OK,
            )
        except:
            return Response(
                {"msg": "Request Failed. Please try again later!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
