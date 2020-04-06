from django.urls import path, include
from rest_framework.routers import DefaultRouter
from beds import views

app_name = "patients"

router = DefaultRouter()
router.register(r'reas', views.ReanimationServiceViewset, basename="reanimation_services")
router.register(r'stays', views.UnitStayViewSet, basename="unit_stays")

urlpatterns = [
    path('', include(router.urls)),
]
