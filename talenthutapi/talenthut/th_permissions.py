from rest_framework.permissions import BasePermission


class IsAdminUserOrPostMethod(BasePermission):
    def has_permission(self, request, view):
        if (request.user and request.user.is_staff) or request.method == 'POST':
            return True

        return False


class IsAdminUserOrRecruiter(BasePermission):

    def has_permission(self, request, view):
        if request.user and (getattr(request.user, 'recruiter', False) or request.user.is_staff):
            return True

        return False


class IsAdminUserOrRecruiterWithPostMethod(BasePermission):

    def has_permission(self, request, view):
        if request.user and ((getattr(request.user, 'recruiter', False) and request.method == "POST")
                             or request.user.is_staff):
            return True

        return False


# This permission class is used for recruiter itself or those activities are related to the recruiter
class IsAdminUserOrRecruiterItself(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            # checks permission for RecruiterDetail view
            is_recruiter_class = getattr(request.user, 'recruiter', False) and request.user.recruiter == obj
            # checks permission for RecruiterActivityDetail view
            is_recruiter_activity_class = getattr(obj, 'recruiter', False) and request.user.recruiter == obj.recruiter

            is_recruiter_itself = is_recruiter_class or is_recruiter_activity_class
            is_admin = request.user.is_staff

        if is_admin or is_recruiter_itself:
            return True

        return False


class IsAdminOrRecruiterOrTalentItself(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            is_recruiter = getattr(request.user, 'recruiter', False)
            is_admin = request.user.is_staff
            is_talent_itself = getattr(request.user, 'talent', False) and request.user.talent == obj

        if is_admin or is_recruiter or is_talent_itself:
            return True

        return False
