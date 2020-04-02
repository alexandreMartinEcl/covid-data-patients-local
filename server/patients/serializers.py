from rest_framework import serializers
from patients.models import Patient, Ventilation
from users.models import get_user_hospital


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        # fields = "__all__"
        exclude = ["hospital"]

    def create(self, validated_data):
        validated_data['inclusion_nb'] = Patient.hash(
            validated_data['inclusion_nb'])
        validated_data['inclusion_code'] = Patient.hash(
            validated_data['inclusion_code'])

        user = self.context.get('request').user
        if user.is_authenticated:
            hospital = get_user_hospital(user)
            if hospital is not None:
                validated_data['hospital'] = hospital
                patient = Patient(**validated_data)
                patient.save()
                return patient
        raise serializers.ValidationError('Unknown hospital')

    def update(self, instance, validated_data):
        validated_data['inclusion_nb'] = instance.inclusion_nb
        validated_data['inclusion_code'] = instance.inclusion_code
        return super(PatientSerializer, self).update(instance, validated_data)


class VentilationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ventilation
        fields = "__all__"
