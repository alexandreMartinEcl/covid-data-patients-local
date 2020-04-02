from django.urls import path, include
from rest_framework.routers import DefaultRouter
from patients import views

app_name = "patients"


router = DefaultRouter()
router.register(r'patients', views.PatientViewset, basename="patients")
router.register(r'ventilations', views.VentilationViewset)

urlpatterns = [
    path('', include(router.urls)),
    path("history/", views.VentilationList.as_view()),
    path("search/", views.PatientList.as_view()),
    path("form/patients/", views.get_patient_form),
    path("form/ventilations/", views.get_ventilation_form),
]
