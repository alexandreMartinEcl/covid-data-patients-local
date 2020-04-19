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


from rest_framework import viewsets, generics, exceptions, status
from patients.models import Patient, Ventilation, StatusMeasure
from patients.serializers import PatientSerializer, VentilationSerializer, StatusMeasureSerializer
from patients.permissions import AuthenticatedAndSafeOrOwnerModification, \
    AuthenticatedAndSafeOrOwnerModificationAttribute
from server import paginations
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import get_user_profile


class PatientViewset(viewsets.ModelViewSet):
    # queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModification]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_queryset(self):
        patients = Patient.objects.all()
        # hospital = get_user_hospital(self.request.user)
        # patients = patients.filter(hospital=hospital)

        user = get_user_profile(self.request.user)
        patients = patients.filter(
            current_reanimation_service__in=user.authorized_reanimation_services.all())

        code = self.request.query_params.get('code', None)
        if code is not None:
            patients = patients.filter(inclusion_nb=code)
        return patients

    def get_serializer_context(self):
        return {'request': self.request}


class PatientList(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModification]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_queryset(self):
        patients = Patient.objects.all()
        # hospital = get_user_hospital(self.request.user)
        # patients = patients.filter(hospital=hospital)

        user = get_user_profile(self.request.user)
        patients = patients.filter(
            current_reanimation_service__in=user.authorized_reanimation_services.all())

        code = self.request.query_params.get('code', None)
        if code is not None:
            patients = patients.filter(inclusion_nb=code)
        return patients


class StatusMeasureViewset(viewsets.ModelViewSet):
    serializer_class = StatusMeasureSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModificationAttribute]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_queryset(self):
        user = get_user_profile(self.request.user)
        measures = StatusMeasure.objects.all()
        measures.filter(reanimation_service__in=user.authorized_reanimation_services.all())

        patient_id = self.request.query_params.get('patient_id', None)
        if patient_id is not None:
            patient = Patient.objects.filter(id=patient_id).first()

            if patient is None:
                raise exceptions.NotFound(f"Patient with id ${patient_id} was not found")
            measures = measures.filter(patient__id=patient_id)

        return measures

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        print(request.data)
        if not is_many:
            return super(StatusMeasureViewset, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class VentilationViewset(viewsets.ModelViewSet):
    queryset = Ventilation.objects.all()
    serializer_class = VentilationSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModificationAttribute]
    pagination_classes = paginations.StandardResultsSetPagination


class VentilationList(generics.ListAPIView):
    serializer_class = VentilationSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModificationAttribute]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Ventilation.objects.all()
        patient = self.request.query_params.get('patients', None)
        if patient is not None:
            queryset = queryset.filter(patient_id=patient).order_by("day")
        return queryset


@api_view(['GET'])
@permission_classes([[AuthenticatedAndSafeOrOwnerModification]])
def get_patient_form(request):
    return Response(Patient.get_react_description())


@api_view(['GET'])
@permission_classes([[AuthenticatedAndSafeOrOwnerModification]])
def get_ventilation_form(request):
    return Response(Ventilation.get_react_description())
