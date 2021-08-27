from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Subject, Course, Tag, Post, Advert, CloudService, ViewsUser, Birthday


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class SubjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ( 'title',)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='Контент')


    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    list_editable = ('is_published',)
    list_filter = ('courses__title', 'subjects__title', 'is_published',)
    list_display_links = ('id', 'title')
    list_display = ('id', 'title','author',
                    'subjects', 'courses', 'created_at',
                    'updated_at', 'get_photo', 'is_published',)
    empty_value_display = "Когда данные столбца пусты, отображение по умолчанию"
    list_max_show_all = 30
    list_per_page = 30

    fields = ('title', 'content',
               'photo',
              'subjects', 'courses',
              'tags',
              'is_published',
              )
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


class AdvertAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Контент')


    class Meta:
        model = Advert
        fields = '__all__'


class AdvertAdmin(admin.ModelAdmin):
    form = AdvertAdminForm
    list_editable = ('is_published',)
    list_filter = ('is_published',)
    list_display_links = ('id', 'content',)
    list_display = ('id', 'content', 'is_published',)
    search_fields = ('content',)


class BirthdayAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget(), label='Верхняя часть поздавления')
    title = forms.CharField(widget=CKEditorWidget(), label='Нижняя часть поздавления')

    class Meta:
        model = Birthday
        fields = '__all__'



class BirthdayAdmin(admin.ModelAdmin):
    form = BirthdayAdminForm
    list_display_links = ('id', 'title',)
    list_display = ('id', 'title',)



class CloudServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'login', 'password', 'extra')
    list_display_links = ('title',)
    search_fields = ('title',)
    fields = ['title', 'login', 'password', 'url', 'image', 'extra']

    def save_model(self, request, obj, form, change):
        if obj.extra is None or obj.extra == '':
            obj.extra = '-'
        return super().save_model(request, obj, form, change)




class ViewsUserAdmin(admin.ModelAdmin):
    model = ViewsUser
    fields = ['last_name_user','first_name_user', 'two_name_user','views_users','uuid_us','date_views' ]
    list_display = ('id', 'last_name_user','first_name_user', 'two_name_user', 'date_views')
    list_display_links =  ('id', 'last_name_user',)


    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     return False




admin.site.register(Course, CourseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Advert, AdvertAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(CloudService, CloudServiceAdmin)
admin.site.register(ViewsUser, ViewsUserAdmin)
admin.site.register(Birthday, BirthdayAdmin)

admin.site.site_header = 'Z0431 - Z0432'

