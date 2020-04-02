from rest_framework import permissions
from users.models import get_user_hospital, get_user_profile, is_valid_hospital


class MedLogPolPermission(permissions.BasePermission):
    message = 'Adding patients not allowed.'

    def has_permission(self, request, view):
        """Check the user can used these method
        
        No check on partenity here
        :param request: [description]
        :type request: [type]
        :param view: [description]
        :type view: [type]
        :returns: [description]
        :rtype: {[type]}
        """
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                hospital = get_user_hospital(request.user)
                profile = get_user_profile(request.user)
                if profile.is_medical:
                    if is_valid_hospital(hospital):
                        return True
        return False

    def has_object_permission(self, request, view, obj):
        """Check that user can use these method on that object.

        When user try to modify object, first has_permission is run and THEN
        object permission
        Here is the check on the paternity
        """

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                hospital = get_user_hospital(request.user)
                profile = get_user_profile(request.user)
                if profile.is_medical:
                    if is_valid_hospital(hospital):
                        return True
        return False
