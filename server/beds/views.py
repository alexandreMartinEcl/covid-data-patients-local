import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, generics, status
from beds.models import ReanimationService, Bed, Unit, UnitStay
from beds.serializers import ReanimationServiceSerializer, UnitStaySerializer, BedSerializer
from beds.permissions import AuthenticatedAndSafeOrOwnerModification, \
    AuthenticatedAndSafeOrOwnerModificationAttribute
from server import paginations
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from beds.models import get_units, get_beds, get_current_unit_stay
from users.models import get_user_reas, get_user_profile
from patients.models import get_patient_with_stay
from rest_framework.response import Response


class ReanimationServiceViewset(viewsets.ModelViewSet):
    # queryset = Patient.objects.all()
    serializer_class = ReanimationServiceSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModification]

    def get_queryset(self):
        access_code = self.request.query_params.get("reanimation_service_code", None)
        if access_code is not None:
            query_set = ReanimationService.objects.filter(access_code=access_code)
            rea = query_set.first()
            if rea is None:
                return query_set

            user = get_user_profile(self.request.user)
            user.authorized_reanimation_services.add(rea)
            user.save()
            reas = query_set
        else:
            reas = get_user_reas(self.request.user)

        return reas

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
