from django.contrib import admin
from django.http import request
from django.utils.safestring import mark_safe
from django.contrib.auth.models import AbstractUser

from .models import Subject, Course, Tag, Post, Advert, CloudService, ViewsUser





class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ( 'title',)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PostAdmin(admin.ModelAdmin):

    list_editable = ('is_published',)
    list_filter = ('courses__title', 'subjects__title', 'is_published',)
    list_display_links = ('id', 'title')
    list_display = ('id', 'title','author',
                    'subjects', 'courses', 'created_at',
                    'updated_at', 'get_photo', 'is_published',)
    list_max_show_all = 30
    list_per_page = 30

    # prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('author', )
    fields = ['title', 'content',
               'photo',
              'subjects', 'courses',
              'tags',
              'is_published',
    ]
    search_fields = ('title', 'courses__title', 'subjects__title', 'content', )

    # date_hierarchy = 'created_at'
    filter_horizontal = ('tags',)



    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src = "{obj.photo.url}" width = "70">')

    get_photo.short_description = 'Миниатюра'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)




class AdvertAdmin(admin.ModelAdmin):
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    list_display_links = ('id', 'content',)
    list_display = ('id', 'content', 'is_published',)
    search_fields = ('content',)


class CloudServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'login', 'password', 'extra')
    list_display_links = ('title',)
    search_fields = ('title',)
    fields = ['title', 'login', 'password', 'url', 'image', 'extra']

class ViewsUserAdmin(admin.ModelAdmin):
    model = ViewsUser
    fields = ['last_name_user','first_name_user', 'two_name_user','views_users' ]
    list_display = ('id', 'last_name_user','first_name_user', 'two_name_user', 'date_user_view', )
    list_display_links =  ('id', 'last_name_user',)


admin.site.register(Course, CourseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(CloudService, CloudServiceAdmin)
admin.site.register(ViewsUser, ViewsUserAdmin)



