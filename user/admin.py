from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CastomUser, Promokod
from .utilites import send_activation_notification


def send_activation(modeladmin, request, queryset):
    for item in queryset:
        if not item.is_activated:
            send_activation_notification(item)
        modeladmin.message_user(request, 'Письма с требованиями активации отправлены')


send_activation.short_description = 'Отправить писма с требованиями активации'


class CastomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'two_name', 'last_name', 'birthday', 'uuid')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_activated', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'last_name', 'first_name', 'two_name', 'birthday', 'is_staff',)

    list_max_show_all = 20
    list_per_page = 20
    readonly_fields = ('uuid',)
    actions = (send_activation,)


class PromokodAdmin(admin.ModelAdmin):
    model = Promokod
    list_display = ('id', 'promo', 'description_promo')
    list_display_links = ('id', 'promo', 'description_promo')


admin.site.register(CastomUser, CastomUserAdmin)
admin.site.register(Promokod, PromokodAdmin)
