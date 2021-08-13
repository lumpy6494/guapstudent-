from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import request

from .models import Post, Subject, Course, Tag


class PostForm(forms.ModelForm):

    subjects = forms.ModelChoiceField( label='' ,empty_label='Выберете предмет', queryset=Subject.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    courses = forms.ModelChoiceField(label='',empty_label= 'Выберете курс', queryset=Course.objects.all(), widget=forms.Select(attrs={'class':'form-control'}))
    # tags = forms.ModelMultipleChoiceField(label='', queryset= Tag.objects.all(), help_text='Для выбора несколькоих тегов зажмите Ctrl',widget=forms.SelectMultiple(attrs={'class': 'form-control','size':'8', 'rows':'8'}))

    class Meta:
        model = Post
        fields = ['title', 'content', 'photo','author', 'subjects', 'courses', 'tags', ]


        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Название',}),
            'content': forms.Textarea(attrs={'class':'form-control','placeholder':'Текст',}),
            'photo' : forms.FileInput(attrs={'class':'form-control',},),
            'tags': forms.SelectMultiple(attrs={'class':'form-control','size': 6, 'rows': 6, 'cols': 6})

        }
        labels = {
            'title': '',
            'content': '',
            'tags':'',
            'photo':'',
        }
        exclude = ('author',)

        help_texts = {
            'tags': 'Для выбора несколькоих тегов зажмите Ctrl',
        }


