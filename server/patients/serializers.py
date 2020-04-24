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

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from rest_framework import serializers

from patients.models import Patient, Ventilation, StatusMeasure
from users.models import get_user_hospital, get_user_profile, UserProfile
from beds.models import UnitStay, Bed, get_current_unit_stay, ReanimationService
from users.serializers import UserSerializer


class StatusMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusMeasure
        fields = "__all__"


class ReducedUnitStaySerializer(serializers.ModelSerializer):
    is_finished = serializers.BooleanField()
    bed_description = serializers.CharField()

    class Meta:
        model = UnitStay
        exclude = ["patient"]


class ReducedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class ReanimationServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReanimationService
        exclude = ["access_code"]


class PatientSerializer(serializers.ModelSerializer):
    bed = serializers.CharField(allow_null=True, allow_blank=True, default=None, write_only=True)
    stay_start_date = serializers.DateField(allow_null=True, write_only=True)
    current_unit_stay = ReducedUnitStaySerializer(read_only=True)
    status_measures = serializers.ListSerializer(child=StatusMeasureSerializer(), read_only=True)
    unit_stays = serializers.ListSerializer(child=ReducedUnitStaySerializer(), read_only=True)
    current_reanimation_service = ReanimationServiceSerializer(read_only=True)
    antecedents = serializers.JSONField(allow_null=True, default='{"NonIndique": ""}')
    allergies = serializers.JSONField(allow_null=True, default='["Non indiqué"]')

    class Meta:
        model = Patient
        fields = "__all__"
        # exclude = ["current_reanimation_service"]

    def create(self, validated_data):
        user = self.context.get('request').user
        if user.is_authenticated:
            # hospital = get_user_hospital(user)
            # if hospital is None:
            #     raise serializers.ValidationError('Unknown hospital')

            # validated_data['hospital'] = hospital
            user = get_user_profile(user)

            assigned_caregivers = validated_data.pop("assigned_caregivers", None)
            bed_id = validated_data.pop("bed", None)
            start_date = validated_data.pop("stay_start_date", None)
            validated_data.pop("stay_id", None)

            patient = Patient(**validated_data)

            if bed_id:
                bed = Bed.objects.filter(id=bed_id).first()
                if bed is None:
                    raise serializers.ValidationError('Bed id (' + bed_id + ') was not found')

                rea = bed.unit.reanimation_service if bed.unit else None

                if rea is None:  # should never happen
                    raise serializers.ValidationError(f'Bed id ({bed_id}) does not belong to a Reanimation service')

                if rea not in user.authorized_reanimation_services.all():
                    raise serializers.ValidationError(f'The bed is in Reanimation {bed_id}, and the user can\'t manage it')
                if bed.is_unusable:
                    raise serializers.ValidationError(f'The bed {bed.unit_index} in Reanimation {bed_id} is not usable')
                if get_current_unit_stay(bed):
                    raise serializers.ValidationError(f'The bed {bed.unit_index} in Reanimation {bed_id} is already occupied')
                patient.current_reanimation_service = rea
                patient.save()
                patient.assigned_caregivers.set(assigned_caregivers)
                UnitStay.objects.create(created_by=user, patient=patient, bed=bed, start_date=start_date)

            else:
                patient.save()
                patient.assigned_caregivers.set(assigned_caregivers)

            return patient
        else:
            raise PermissionDenied

    def update(self, instance, validated_data):
        todo_list = validated_data.pop("todo_list", None)
        treatment_limitations = validated_data.pop("treatment_limitations", None)
        recent_disease_history = validated_data.pop("recent_disease_history", None)
        evolution = validated_data.pop("evolution", None)
        day_notice = validated_data.pop("day_notice", None)

        if todo_list:
            validated_data["todo_list"] = todo_list
            validated_data["last_edited_todo_list"] = timezone.now()

        if recent_disease_history:
            validated_data["recent_disease_history"] = recent_disease_history
            validated_data["last_edited_recent_disease_history"] = timezone.now()

        if evolution:
            validated_data["evolution"] = evolution
            validated_data["last_edited_evolution"] = timezone.now()

        if treatment_limitations:
            validated_data["treatment_limitations"] = treatment_limitations
            validated_data["last_edited_treatment_limitations"] = timezone.now()

        if day_notice:
            validated_data["day_notice"] = day_notice
            validated_data["last_edited_day_notice"] = timezone.now()

        return super(PatientSerializer, self).update(instance, validated_data)


class BasicInfoPatientSerializer(PatientSerializer):
    bed = serializers.CharField(allow_null=True, allow_blank=True, default=None)
    current_unit_stay = None
    status_measures = None
    unit_stays = None
    antecedents = None
    allergies = None
    current_reanimation_service = ReanimationServiceSerializer()

    class Meta:
        model = Patient
        # fields = "__all__"
        exclude = ["detection_covid", "detection_orlEntree", "detection_ERentree", "detection_ERpremierMardi",
                   "detection_ERsecondMardi", "antecedents", "allergies", "recent_disease_history", "evolution"]


class StatusMeasureSerializer(serializers.ModelSerializer):
    id_patient = serializers.CharField()
    id_reanimation_service = serializers.CharField(read_only=True)
    created_by = ReducedUserSerializer(read_only=True)

    class Meta:
        model = StatusMeasure
        fields = ["created_date", "status_type", "value", "id_reanimation_service", "created_by", "id_patient"]
        # exclude = ["patient", "reanimation_service", ""]

    def create(self, validated_data):
        user = self.context.get('request').user
        user = get_user_profile(user)

        id_patient = validated_data.pop("id_patient", None)
        if id_patient is None:
            raise serializers.ValidationError('Vous devez fournir id_patient dans les données')

        patient = Patient.objects.filter(id=id_patient).first()
        if patient is None:
            raise serializers.ValidationError(f'Patien ({id_patient}) introuvable')

        if patient.current_unit_stay is None:
            raise serializers.ValidationError(f'Patient {id_patient} pas actuellement en réanimation.')

        try:
            rea = patient.current_unit_stay.bed.unit.reanimation_service
        except:
            # should not happen
            raise serializers.ValidationError('Le patient est en réanimation, mais '
                                              'le service de réa est introuvable')

        if rea not in user.authorized_reanimation_services.all():
            raise serializers.ValidationError(f'Le patient est en réanimation, dans le service {rea}. '
                                              f'Vous n\'avez pas accès à ce service')

        matching_measure = StatusMeasure.objects.filter(patient=patient)\
            .filter(status_type=validated_data["status_type"])\
            .filter(created_date=validated_data["created_date"])\
            .filter(reanimation_service=rea)\
            .first()

        if matching_measure:
            matching_measure.value = validated_data["value"]
            matching_measure.created_by = user
            matching_measure.save()
            return matching_measure
        else:
            validated_data["reanimation_service"] = rea
            validated_data["patient"] = patient
            validated_data["created_by"] = user
            measure = StatusMeasure(**validated_data)
            measure.save()
            return measure


class VentilationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventilation
        fields = "__all__"
