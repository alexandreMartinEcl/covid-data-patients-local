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

from django.urls import path
from web.views import index, opendata, add_paper, stock, export_csv, \
    registration, registration_done

app_name = "web"


urlpatterns = [
    path("opendata/", opendata, name="opendata"),
    path("opendata/add/", add_paper, name="add_paper"),
    path("opendata/add/<str:obj>/", add_paper, name="add_paper"),
    path("stock/", stock, name="stock"),
    path("visu/", export_csv, name="all_hospital"),
    path("", index, name="index"),
    path("registration/", registration, name="registration"),
    path("registration/done", registration_done, name="registrtion_none"),
]
