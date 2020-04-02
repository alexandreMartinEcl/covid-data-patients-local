from django.contrib import admin
from maj.models import MAJ


class MAJAdmin(admin.ModelAdmin):
    pass


admin.site.register(MAJ, MAJAdmin)
