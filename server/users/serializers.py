from rest_framework import serializers
from users.models import Hospital


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
        # exclude = ["phone_bed_manager"]

    def validate(self, data):
        raise serializers.ValidationError("Edition of Hospital not authorized")
