import json

from django.core.exceptions import PermissionDenied
from django.utils.datetime_safe import date
from rest_framework import serializers
from beds.models import ReanimationService, UnitStay, Bed, Unit, get_reanimation_service_from_bed
from users.models import get_user_reas
from patients.serializers import PatientSerializer, BasicInfoPatientSerializer


class UnitStaySerializer(serializers.ModelSerializer):
    patient = BasicInfoPatientSerializer()
    id_bed = serializers.CharField(write_only=True)
    terminate = serializers.BooleanField(write_only=True)
    bed_description = serializers.CharField()

    class Meta:
        model = UnitStay
        fields= "__all__"
        read_only_fields = ["end_date", "bed", "bed_description"]

    def update(self, instance, validated_data):
        user = self.context.get('request').user

        authorized_reas = get_user_reas(user).all()
        rea = instance.bed.unit.reanimation_service
        if rea is None:
            raise serializers.ValidationError('The reanimation service could not be found.')

        if rea not in authorized_reas:
            raise PermissionDenied

        new_bed_id = validated_data.pop("id_bed", None)
        if new_bed_id:
            if int(new_bed_id) != instance.bed.id:
                new_bed = Bed.objects.filter(id=new_bed_id).first()
                if new_bed is None:
                    raise serializers.ValidationError(f"Le lit demandé (${new_bed_id}) n'existe pas")

                new_bed_rea = new_bed.unit.reanimation_service
                if new_bed_rea not in authorized_reas:
                    raise serializers.ValidationError(f"Le lit demandé (${new_bed_id}) appartien au "
                                                      f"service ${new_bed_rea}. Vous n'avez pas les accès.")

                if new_bed.current_stay:
                    raise serializers.ValidationError(f"Le lit demandé (${new_bed_id}) est déjà occupé.")

                if new_bed.is_unusable:
                    raise serializers.ValidationError(f"Le lit demandé (${new_bed_id}) n'est pas en état de service.")

                validated_data["bed"] = new_bed

        terminate = validated_data.pop("terminate", None)
        if terminate:
            validated_data["end_date"] = date.today()
        return super(UnitStaySerializer, self).update(instance, validated_data)


class BedSerializer(serializers.ModelSerializer):
    current_stay = UnitStaySerializer()

    class Meta:
        model = Bed
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    beds = serializers.ListSerializer(child=BedSerializer())

    class Meta:
        model = Unit
        fields = "__all__"


class ReanimationServiceSerializer(serializers.ModelSerializer):
    units = serializers.ListSerializer(child=UnitSerializer())

    class Meta:
        model = ReanimationService
        # fields = "__all__"
        exclude = ["access_code"]
