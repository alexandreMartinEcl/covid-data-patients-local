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

from django.http import HttpResponseForbidden, HttpResponse
from rest_framework.authentication import BaseAuthentication

from users.models import User, get_or_create_user


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class FreeAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # header = self.get_header(request)
        # if header is None:
        #     return None
        #
        raw_token = ""  # self.get_raw_token(header)
        # if raw_token is None:
        #     return None
        #
        # if type(raw_token) == bytes:
        #     raw_token = raw_token.decode('utf-8')
        #
        # try:
        #     payload = IDServer.verify_jwt(raw_token)
        # except ValueError:
        #     return HttpResponseUnauthorized('<h1>401 Invalid or expired JWT token</h1>', content_type='text/html')
        # try:
        u = User.objects.get(username='user1')
        return u, raw_token
        # except ObjectDoesNotExist:
        #     user = get_or_create_user(jwt_access_token=raw_token)
        #     return user, raw_token

    # def get_header(self, request):
    #     """
    #     Extracts the header containing the JSON web token from the given
    #     request.
    #     """
    #     header = request.META.get('HTTP_AUTHORIZATION')
    #
    #     if isinstance(header, str):
    #         # Work around django test client oddness
    #         header = header.encode(HTTP_HEADER_ENCODING)
    #
    #     return header
    #
    # def get_raw_token(self, header):
    #     """
    #     Extracts an unvalidated JSON web token from the given "Authorization"
    #     header value.
    #     """
    #     parts = header.split()
    #
    #     if len(parts) == 0:
    #         # Empty AUTHORIZATION header sent
    #         return None
    #
    #     if parts[0] not in AUTH_HEADER_TYPE_BYTES:
    #         # Assume the header does not contain a JSON web token
    #         return None
    #
    #     if len(parts) != 2:
    #         raise AuthenticationFailed(
    #             _('Authorization header must contain two space-delimited values'),
    #             code='bad_authorization_header',
    #         )
    #
    #     return parts[1]