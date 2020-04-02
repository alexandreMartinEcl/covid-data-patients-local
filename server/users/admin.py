from django.contrib import admin
from users.models import Hospital, UserProfile


class HospitalAdmin(admin.ModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Hospital, HospitalAdmin)
