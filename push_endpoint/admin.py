from django.contrib import admin
from push_endpoint.models import PushedData
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


from push_endpoint.models import Provider


class ProviderInline(admin.StackedInline):
    model = Provider
    can_delete = False
    verbose_name = 'provider'


class UserAdmin(UserAdmin):
    inlines = (ProviderInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(PushedData)
