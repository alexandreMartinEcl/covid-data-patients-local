from rest_framework import permissions
from users.models import get_user_hospital, get_user_profile, is_valid_hospital


class AuthenticatedAndSafeOrOwnerModification(permissions.BasePermission):
    message = 'Adding reas not allowed.'

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
                return True
        return False

    def has_object_permission(self, request, view, obj):
        """Check that user can use these method on that object.
        
        When user try to modify object, first has_permission is run and THEN
        object permission
        Here is the check on the paternity
        """
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return False


class AuthenticatedAndSafeOrOwnerModificationAttribute(
        permissions.BasePermission):
    message = 'Adding ventilation not allowed.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS + ("POST",
                                                         "PUT", "PATCH"):
            if request.user.is_authenticated:
                # hospital = get_user_hospital(request.user)
                # if hospital is not None:
                #     return True
                return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                # hospital = get_user_hospital(request.user)
                # profile = get_user_profile(request.user)
                # if is_valid_hospital(hospital) and profile.is_medical:
                #     return True
                user = get_user_profile(request.user)
                return obj.bed.unit.reanimation_service in \
                       user.authorized_reanimation_services.all()

        elif request.method in ["PUT", "PATCH"]:
            # if request.user.is_authenticated:
            #     hospital = get_user_hospital(request.user)
            #     profile = get_user_profile(request.user)
            #     if is_valid_hospital(hospital) and profile.is_medical:
            #         return obj.patient.hospital == hospital
                user = get_user_profile(request.user)
                return obj.bed.unit.reanimation_service in \
                       user.authorized_reanimation_services.all()

        return False
