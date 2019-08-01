from django.contrib import admin
from django.contrib.auth.admin import Group
from django.contrib.auth import get_user_model
from .models import User, UserProfile
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'batch',
                    'class_id', 'id_card_number', 'department')
    list_filter = ('batch', 'id_card_number', 'department')

    search_fields = ('email', 'full_name',)


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.unregister(Group)
