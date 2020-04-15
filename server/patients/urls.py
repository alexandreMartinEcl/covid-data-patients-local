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

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients import views

app_name = "patients"

router = DefaultRouter()
router.register(r'infos', views.PatientViewset, basename="patients")

router.register(r'status_measures', views.StatusMeasureViewset, basename="statusmeasures")
router.register(r'ventilations', views.VentilationViewset)

urlpatterns = [
    path('', include(router.urls)),
    path("history/", views.VentilationList.as_view()),
    path("search/", views.PatientList.as_view()),
    path("form/patients/", views.get_patient_form),
    path("form/ventilations/", views.get_ventilation_form),
]
