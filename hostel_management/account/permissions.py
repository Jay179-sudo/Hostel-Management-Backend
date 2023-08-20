from rest_framework import permissions
import jwt
from .models import User
import os


class SuperAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        trial = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms="HS256")
        user = User.objects.get(id=trial["user_id"])
        if user.isSuperAdmin:
            return True
        return False


class HostelAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.META)
        token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        trial = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms="HS256")
        user = User.objects.get(id=trial["user_id"])
        print("Why ", user)
        if user.isHostelAdmin:
            return True
        return False


class StudentOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        trial = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms="HS256")
        user = User.objects.get(id=trial["user_id"])
        if user.isStudent:
            return True
        return False


class MessManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        trial = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms="HS256")
        user = User.objects.get(id=trial["user_id"])
        if user.isMessManager:
            return True
        return False
