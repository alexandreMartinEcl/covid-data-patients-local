from django.contrib import admin
from patients.models import Patient, Ventilation


class PatientAdmin(admin.ModelAdmin):
    pass


class VentilationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Patient, PatientAdmin)
admin.site.register(Ventilation, VentilationAdmin)
