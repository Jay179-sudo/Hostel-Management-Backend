from django.urls import path, include
from .views import (
    SuperAdminRegister,
    HostelRegister,
    HostelAdminRegister,
    MessManagerRegister,
    StudentRegister,
    SuperAdminLoginView,
    HostelAdminLogin,
    StudentLogin,
    MessManagerLogin,
    UserProfileView,
    UserChangePasswordView,
    SendPasswordResetEmail,
    UserPasswordResetView,
    CreateReadLeaveRequestsStudent,
    UpdateRoomAllocation,
    ListStudentsPresentView,
    UploadCSV,
    viewStudentsPresentYesterday,
    AbsentDaysView,
    createabsentrecord,
    getRoomFromEmail,
    getRoomDetails,
    occupiedRooms,
    unoccupiedRooms,
    AbsentDaysSpecificView,
    AbsentToday,
    listLeaveRequests,
    getsUserType,
    deleteAbsent,
    checkAbsentRecord,
    GetAttendanceCSVViewSet,
)

urlpatterns = [
    path(
        "superadminregister/", SuperAdminRegister.as_view(), name="super_admin_register"
    ),  # done FE
    path("hostelregister/", HostelRegister.as_view(), name="hostel_register"),
    path(
        "hosteladminregister/",
        HostelAdminRegister.as_view(),
        name="hostel_admin_register",
    ),  # done FE
    path(
        "messmanagerregister/",
        MessManagerRegister.as_view(),
        name="mess_manager_register",
    ),  # done FE
    path(
        "studentregister/",
        StudentRegister.as_view(),
        name="student_register",  # done FE
    ),
    path(
        "superadminlogin/", SuperAdminLoginView.as_view(), name="super_admin_login"
    ),  # done FE
    path(
        "hosteladminlogin/", HostelAdminLogin.as_view(), name="hostel_admin_login"
    ),  # done FE1
    path("studentlogin/", StudentLogin.as_view(), name="student_login"),  # done FE
    path("messmanagerlogin/", MessManagerLogin.as_view(), name="mess_login"),  # done FE
    path("profile/", UserProfileView.as_view(), name="profile"),  # done FE
    path(
        "changepassword/", UserChangePasswordView.as_view(), name="change_password"
    ),  # done FE
    path(
        "sendresetpasswordemail/",
        SendPasswordResetEmail.as_view(),
        name="reset_email",  # done FE
    ),
    path(
        "reset-password/<uid>/<token>/",
        UserPasswordResetView.as_view(),
        name="change_password",  # done FE
    ),
    # student view
    path(
        "studentleavereq/",
        CreateReadLeaveRequestsStudent.as_view(),
        name="student_leave_req",
    ),  # done FE
    # hostel admin
    path(
        "hosteladminroomallocation/",
        UpdateRoomAllocation.as_view(),
        name="hostel_admin_update_room",
    ),
    path("liststudentstoday/", ListStudentsPresentView.as_view(), name="list_students"),
    # ___________NEW URLS________________
    path("uploadcsv/", UploadCSV.as_view(), name="upload-csv"),  # done FE
    path(
        "viewstudentspresentyesterday/",
        viewStudentsPresentYesterday.as_view(),
        name="viewStudentsPresentYesterday",
    ),
    path(
        "AbsentDaysView/",
        AbsentDaysView.as_view(),
        name="daterangeStudentList",
    ),
    path(
        "createabsentrecord/", createabsentrecord.as_view(), name="createabsentrecord"
    ),
    path("getemailfromroom/", getRoomFromEmail.as_view(), name="get-room-from-email"),
    path("getroomdetails/", getRoomDetails.as_view(), name="get-room-details"),
    path("occupiedRooms/", occupiedRooms.as_view(), name="occupied-rooms"),
    path("unoccupiedRooms/", unoccupiedRooms.as_view(), name="unoccupied-rooms"),
    path(
        "AbsentDaysSpecificView/",
        AbsentDaysSpecificView.as_view(),
        name="absent-days-spec-view",
    ),
    path("absenttoday/", AbsentToday.as_view(), name="Absent Today"),
    path("listleaverequests/", listLeaveRequests.as_view(), name="List Leave Requests"),
    path("getusertype/", getsUserType.as_view(), name="get_user_type"),
    path("deleteAbsentRecord/", deleteAbsent.as_view(), name="delete-absent-record"),
    path("checkAbsentRecord/", checkAbsentRecord.as_view(), name="check-absent-record"),
    path(
        "getattendancecsv/",
        GetAttendanceCSVViewSet.as_view(),
        name="get-attendance-csv",
    ),
]
