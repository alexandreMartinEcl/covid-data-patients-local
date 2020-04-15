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

from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from users.models import Hospital, get_sentinel_hospital, UserProfile
from users.serializers import HospitalSerializer, UserProfileSerializer
from users.permissions import MedLogPolPermission, AuthenticatedAndSafeOrOwnerModification
from server import paginations
from rest_framework.response import Response


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AuthenticatedAndSafeOrOwnerModification]
    pagination_classes = paginations.StandardResultsSetPagination

    def get_serializer_context(self):
        return {'request': self.request}

    def partial_update(self, request, pk=None):
        user = self.get_object()
        # print(request.data.dict())
        serializer = self.serializer_class(user, data=request.data, partial=True)  #, context={'request_data': request.data})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
