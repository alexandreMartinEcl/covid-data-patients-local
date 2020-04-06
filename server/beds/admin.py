from django.contrib import admin
from beds.models import ReanimationService, UnitStay, Unit, Bed


class ReanimationServiceAdmin(admin.ModelAdmin):
    pass


class UnitStayAdmin(admin.ModelAdmin):
    pass


class UnitAdmin(admin.ModelAdmin):
    pass


class BedAdmin(admin.ModelAdmin):
    pass


admin.site.register(ReanimationService, ReanimationServiceAdmin)
admin.site.register(UnitStay, UnitStayAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Bed, BedAdmin)
