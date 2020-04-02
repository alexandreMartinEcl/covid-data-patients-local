from rest_framework import viewsets, generics
from patients.models import Patient, Ventilation
from patients.serializers import PatientSerializer, VentilationSerializer
from patients.permissions import AuthenticatedAndSafeOrOwnerModification, \
    AuthenticatedAndSafeOrOwnerModificationAttribute
from server import paginations
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from users.models import get_user_hospital


class PatientViewset(viewsets.ModelViewSet):
    # queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModification]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_queryset(self):
        patients = Patient.objects.all()
        hospital = get_user_hospital(self.request.user)
        patients = patients.filter(hospital=hospital)
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
        hospital = get_user_hospital(self.request.user)
        patients = patients.filter(hospital=hospital)
        code = self.request.query_params.get('code', None)
        if code is not None:
            patients = patients.filter(inclusion_nb=code)
        return patients


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
