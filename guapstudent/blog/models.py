from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify


class Course(models.Model):
    '''Модель курса'''
    title = models.CharField(max_length=100, verbose_name='Курс')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL Курса')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Subject(models.Model):
    '''Модель Предмета'''

    title = models.CharField(max_length=250, verbose_name='Предмет')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL Предмета')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    course_sub = models.ManyToManyField(Course, related_name='course_sub', verbose_name='Курсы предмета')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('subject', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['-created_at']


class Tag(models.Model):
    '''Модель Тегов'''
    title = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL Тега')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']


class Post(models.Model):
    '''Модель Постов'''

    title = models.CharField(max_length=255, verbose_name='Пост')
    # slug = models.SlugField(max_length=100, unique=True, verbose_name='URL Проста')
    content = models.TextField(blank=True, verbose_name='Контент')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор', editable=False, blank=True, null=True )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', verbose_name='Миниатюра', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    subjects = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='posts', verbose_name='Предмет')
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='posts', verbose_name='Курс', )
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Теги', )
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']


class Advert(models.Model):
    '''Модель Объявления'''

    content = models.TextField(blank=True, max_length=300, verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата Объявления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return " Объявлениe "

    class Meta:
        verbose_name = 'Объявления'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']


class CloudService(models.Model):
    " Модель Сервиса "
    title = models.CharField(max_length=255, verbose_name="Название сервиса")
    login = models.CharField(max_length=255, verbose_name="Логин сервиса")
    password = models.CharField(max_length=255, verbose_name="Пароль для сервиса")
    image = models.ImageField(upload_to='photo/%Y/%m/%d', verbose_name='Картинка', blank= True )
    extra = models.TextField(blank=True, verbose_name='Дополнительная информация')
    url = models.URLField(verbose_name='Ссылка', blank= True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Сервис(Облако)'
        verbose_name_plural = 'Сервисы'
        ordering = ['title']
