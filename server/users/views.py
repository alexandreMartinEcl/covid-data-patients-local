from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from users.models import Hospital, get_sentinel_hospital
from users.serializers import HospitalSerializer
from users.permissions import MedLogPolPermission
from server import paginations
from rest_framework.response import Response
from rest_framework import status


class HospitalView(generics.ListAPIView):
    serializer_class = HospitalSerializer
    permission_classes = [MedLogPolPermission]
    pagination_classes = paginations.StandardResultsSetPagination
    # add renderers ?

    def get_queryset(self):
        query = Hospital.objects.all().exclude(id=get_sentinel_hospital().id)
        # code = self.request.query_params.get('state', None)
        # if code is not None:
        #     patients = patients.filter(inclusion_nb=code)
        return query


@api_view(['GET'])
@permission_classes([MedLogPolPermission])
def get_hospital_form(request):
    return Response(Hospital.get_react_description())
