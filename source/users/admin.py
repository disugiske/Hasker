from django.contrib import admin

from users.models import Profile

class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_active", "last_login")

admin.site.register(Profile, UsersAdmin)
