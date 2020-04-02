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
