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

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from server.utils import get_field_schema
from django.utils.translation import gettext_lazy as _

import django.db.models.fields as fields


def get_or_create_user(user_info):
    # user_info = IDServer.check_ids(username=username, password=password)
    user = User.objects.filter(username=user_info["username"]).first()

    if user is None:
        user = User(
            username=user_info['username'],
            email=user_info['email'],
            first_name=user_info['firstname'][:30],
            last_name=user_info['lastname'][:30],
        )

    user.is_active = True
    user.save()  # will update or insert
    user_profile = UserProfile(user=user, username=user.username)
    user_profile.save()
    return user


def get_user_reas(user: User):
    profile = get_user_profile(user)
    if profile is None:
        return None
    else:
        return profile.authorized_reanimation_services.all()


def get_sentinel_hospital():
    return Hospital.objects.get_or_create(
        full_name="deleted", phone_bed_manager="12345678")[0]


def get_user_hospital(user: User):
    """Return the hospital associated with the user

    If no Hospital is found return None. If user not authenticated
    raise permission denied
    :param user: The user whom we want the hospital
    :type user: User
    """
    profile = get_user_profile(user)
    if profile is None:
        return None
    else:
        return profile.hospital


class UserProfile(models.Model):
    username = models.CharField(max_length=7, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # is_medical = models.BooleanField(default=False)
    # hospital = models.ForeignKey(
    #     "Hospital", on_delete=models.SET(get_sentinel_hospital))
    title = models.CharField(blank=True, null=True, choices=[('M', 'Médical'), ('K', 'Kinésithérapeute'),
                                                 ('AS', 'Aide soignant'), ('I', 'Infirmier')], max_length=30)
    authorized_reanimation_services = models.ManyToManyField("beds.ReanimationService", blank=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.user.last_name} ({self.title})"  # (Hôpital {self.hospital})"
    # def __str__(self):
    #     status = ""
    #     if self.is_medical:
    #         status += " M"
    #     elif self.is_logistic:
    #         status += ' L'
    #     elif self.is_politic:
    #         status += " P"
    #
    #     return self.user.username + status


def get_user_profile(user: User) -> UserProfile:
    """Return the UserProfile associated with the user

    If no UserProfile is found return None. If user not authenticated
    raise permission denied
    :param user: The user whom we want the Userprofile
    :type user: User
    """
    if user.is_authenticated:
        profile = UserProfile.objects.filter(user=user).first()
        return profile
    else:
        raise PermissionDenied


class Hospital(models.Model):
    full_name = models.CharField(max_length=500)
    latitude = models.FloatField(default=48.856614)
    longitude = models.FloatField(default=2.3522219)
    postcode = models.CharField(max_length=50)
    phone_bed_manager = models.CharField(max_length=500)
    country = models.CharField(max_length=50, default="FRANCE")

    def __str__(self):
        return f"Hôpital {self.full_name}"

    @classmethod
    def get_react_description(cls):
        required = []
        json_schema = {
            "title": _("Descriptif de l'établissement"),
            "description": _("Descriptif de l'établissement"),
            "type": "object",
            "required": required,
            "properties": {
            }
        }

        all_fields = cls._meta.fields

        translations = {}
        for field in all_fields:
            translations[field.name] = field.name

        translations["full_name"] = _("Établissement")
        translations["latitude"] = _("Latitude")
        translations["longitude"] = _("Longitude")
        translations["country"] = _("Pays")
        translations["postcode"] = _("Code Postal")
        translations["phone_bed_manager"] = _("Contact Gestionnaire")

        for field in all_fields:
            # if field.name in []:
            #     continue
            local_json_schema = get_field_schema(field,
                                                 translations[field.name])
            json_schema['properties'][field.name] = local_json_schema
            if not field.blank and type(field) is not fields.BooleanField:
                required.append(field.name)

        return json_schema


def is_valid_hospital(hospital: Hospital):
    # We don't want old data (due to deleted hospital to change)
    if hospital is None or hospital == get_sentinel_hospital():
        return False
    else:
        return True
