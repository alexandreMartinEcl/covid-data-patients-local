from django.forms import ModelForm
from patients.models import Patient, Ventilation


class PatientForm(ModelForm):
    class Meta:
        model = Patient
        # fields = "__all__"
        exclude = ['hospital']
        labels = {
            'age': ('Age'),
        }
        help_texts = {
            'age': ('En années.'),
        }
        # error_messages = {
        #     'name': {
        #         'max_length': ("This writer's name is too long."),
        #     },
        # }

    def validate(self, data):
        validated_data = super(PatientForm).validate(data)
        validated_data['inclusion_code'] = Patient.hash(
            validated_data['inclusion_code'])
        validated_data['inclusion_nb'] = Patient.hash(
            validated_data['inclusion_nb'])
        return validated_data


class VentilationForm(ModelForm):
    class Meta:
        model = Ventilation
        fields = "__all__"
