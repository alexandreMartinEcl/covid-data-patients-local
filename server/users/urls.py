from django.urls import path, include
# from rest_framework.routers import DefaultRouter
from users import views

app_name = "users"

# router = DefaultRouter()
# router.register(r"hospitals", views.HospitalView, basename="hospitals")

urlpatterns = [
    path('hospitals/', views.HospitalView.as_view(), name="hospitals"),
    path("form/", views.get_hospital_form, name="hospital_form"),
]
