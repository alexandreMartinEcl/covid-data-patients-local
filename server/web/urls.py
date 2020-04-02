from django.urls import path
from web.views import index, opendata, add_paper, stock, export_csv, registration, registration_done

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
