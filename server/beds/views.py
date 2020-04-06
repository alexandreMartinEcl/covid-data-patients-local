import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics
from beds.models import ReanimationService, Bed, Unit, UnitStay
from beds.serializers import ReanimationServiceSerializer, UnitStaySerializer, BedSerializer
from beds.permissions import AuthenticatedAndSafeOrOwnerModification, \
    AuthenticatedAndSafeOrOwnerModificationAttribute
from server import paginations
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from beds.models import get_units, get_beds, get_current_unit_stay
from users.models import get_user_reas
from patients.models import get_patient_with_stay
from rest_framework.response import Response


class ReanimationServiceViewset(viewsets.ModelViewSet):
    # queryset = Patient.objects.all()
    serializer_class = ReanimationServiceSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModification]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_queryset(self):
        # reas = ReanimationService.objects.all()
        authorized_reas = get_user_reas(self.request.user)
        # if external_code is not None:
        #     authorized_reas = authorized_reas.filter(id=external_code)
        return authorized_reas

    def get_serializer_context(self):
        return {'request': self.request}


class UnitStayViewSet(viewsets.ModelViewSet):
    serializer_class = UnitStaySerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModificationAttribute]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_queryset(self):
        stays = UnitStay.objects.all()
        authorized_reas = get_user_reas(self.request.user)
        stays.filter(bed__unit__reanimation_service__in=authorized_reas)
        return stays

    def partial_update(self, request, pk=None):
        stay = self.get_object()
        serializer = self.serializer_class(stay, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
