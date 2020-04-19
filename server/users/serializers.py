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

from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Hospital, UserProfile

from beds.models import ReanimationService


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
        # exclude = ["phone_bed_manager"]

    def validate(self, data):
        raise serializers.ValidationError("Edition of Hospital not authorized")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ReducedReanimationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReanimationService
        fields = "__all__"
        excluded = ["units"]


class UserProfileSerializer(serializers.ModelSerializer):
    reanimation_service_code = serializers.CharField(write_only=True)
    authorized_reanimation_services = serializers.ListSerializer(child=ReducedReanimationServiceSerializer())

    class Meta:
        model = UserProfile
        fields = "__all__"
        read_only_fields = ["user", "username", "authorized_reanimation_services"]

    def update(self, instance, validated_data):
        reanimation_service_code = validated_data.pop("reanimation_service_code", None)
        if reanimation_service_code is not None:
            rea = ReanimationService.objects.filter(access_code=reanimation_service_code).first()
            if not rea:
                raise serializers.ValidationError("The code for reanimation service is wrong")

            reas = instance.authorized_reanimation_services
            reas.add(rea)
            validated_data["authorized_reanimation_services"] = reas.all()
        return super(UserProfileSerializer, self).update(instance, validated_data)

