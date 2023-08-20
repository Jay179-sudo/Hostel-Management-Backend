from django.contrib import admin

# Register your models here.
from .models import (
    User,
    Student,
    LeaveRequest,
    Hostel,
    HostelAdmin,
    MessManager,
    SuperAdmin,
    AbsentAttendance,
    HostelRoom,
)

admin.site.register(User)
admin.site.register(Student)
admin.site.register(LeaveRequest)
admin.site.register(Hostel)
admin.site.register(HostelAdmin)
admin.site.register(MessManager)
admin.site.register(SuperAdmin)
admin.site.register(AbsentAttendance)
admin.site.register(HostelRoom)
