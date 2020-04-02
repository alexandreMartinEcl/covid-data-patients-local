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
