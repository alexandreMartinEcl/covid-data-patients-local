"""
Copyright (c) 2020 Magic LEMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from rest_framework import permissions
from users.models import get_user_profile


class AuthenticatedAndSafeOrOwnerModification(permissions.BasePermission):
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
        if request.method in permissions.SAFE_METHODS + ("POST",
                                                         "PUT", "PATCH"):
            if request.user.is_authenticated:
                # hospital = get_user_hospital(request.user)
                # profile = get_user_profile(request.user)
                # if is_valid_hospital(hospital) and profile.is_medical:
                #     return True
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

        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                # hospital = get_user_hospital(request.user)
                # profile = get_user_profile(request.user)
                # if is_valid_hospital(hospital) and profile.is_medical:
                #     return True
                return True

        elif request.method in ["PUT", "PATCH"]:
            if request.user.is_authenticated:
                user = get_user_profile(request.user)
                if obj.current_unit_stay is not None:
                    return obj.current_unit_stay.bed.unit.reanimation_service in user.authorized_reanimation_services.all()
                # hospital = get_user_hospital(request.user)
                # profile = get_user_profile(request.user)
                # if is_valid_hospital(hospital) and profile.is_medical:
                #     return obj.hospital == hospital

        return False


class AuthenticatedAndSafeOrOwnerModificationAttribute(permissions.BasePermission):
    message = 'Adding status measure not allowed.'
    # message = 'Vous devez être assigné à un service de réanimation où le patient demandé à séjourné. ' \
    #           'Pensez à fournir le patient_id en paramètre'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS + ("POST",
                                                         "PUT", "PATCH"):
            if request.user.is_authenticated:
                return True
                # hospital = get_user_hospital(request.user)
                # if hospital is not None:
                #     return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_authenticated:
                # hospital = get_user_hospital(request.user)
                # profile = get_user_profile(request.user)
                # if is_valid_hospital(hospital) and profile.is_medical:
                #     return obj.patient.hospital == hospital
                user = get_user_profile(self.request.user)
                return obj.patient.current_unit_stay.bed.unit.reanimation_service in \
                       user.authorized_reanimation_services.all()

        elif request.method in ["PUT", "PATCH"]:
            if request.user.is_authenticated:
                # hospital = get_user_hospital(request.user)
                # profile = get_user_profile(request.user)
                # if is_valid_hospital(hospital) and profile.is_medical:
                #     return obj.patient.hospital == hospital
                user = get_user_profile(self.request.user)
                return obj.patient.current_unit_stay.bed.unit.reanimation_service in \
                       user.authorized_reanimation_services.all()

        return False
