from django.contrib import admin
from authorization import models


class UserAdmin(admin.ModelAdmin):
    def full_name(self):
        return self.get_full_name()

    list_display = ('username', full_name, 'groups', 'is_active', 'is_staff')
    list_filter = ['groups', 'is_active', 'is_staff']
    search_fields = ['id', 'username', 'first_name', 'last_name']


admin.site.register(models.User, UserAdmin)
