from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CastomUser, Promokod


class CastomUserAdmin(UserAdmin):
    model = CastomUser

    list_display = ('username', 'email',  'last_name', 'first_name', 'two_name', 'is_staff')




class PromokodAdmin(admin.ModelAdmin):

    model = Promokod
    list_display = ('id', 'promo', 'description_promo')
    list_display_links = ('id', 'promo', 'description_promo')



admin.site.register(CastomUser,CastomUserAdmin)
admin.site.register(Promokod, PromokodAdmin)
