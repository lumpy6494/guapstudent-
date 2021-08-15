from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CastomUser(AbstractUser):
    two_name = models.CharField(max_length= 255, verbose_name='Отчество')
    birthday = models.DateField(blank=True, null=True, verbose_name='День Рождения')


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Promokod(models.Model):
    promo = models.CharField(max_length=50, verbose_name='Пригласительный', blank=True, null=True)
    description_promo = models.TextField(max_length=500, verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.promo

    class Meta:
        verbose_name = 'Пригласительный '
        verbose_name_plural = 'Пригласительные'



