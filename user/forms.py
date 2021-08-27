from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django import forms
from .models import CastomUser


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин'}))
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))

    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))

    two_name = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество'})
    )
    last_name = forms.CharField(
        help_text='Укажите Ваше реальные ФИО чтобы получить доступ к скрытой информации',
        label='',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}))

    birthday = forms.DateField(
        required=False,
        label='',
        help_text='Необязятельное поле',
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'День Вашего Рождения'})
    )

    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}))

    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}))

    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'}))

    promo = forms.CharField(required=False,
                            help_text='Пригласительный если есть (Необязятельное поле)',
                            label='',
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пригласительный'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False
        user.is_activated =False
        if commit:
            user.save()
        return user
    class Meta:
        model = CastomUser
        fields = ['username', 'first_name', 'two_name', 'last_name', 'birthday', 'email', 'password1', 'password2',
                  'promo']


class UpadateUserForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    two_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        help_text='Укажите Ваше реальные ФИО чтобы получить доступ к скрытой информации',
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    birthday = forms.DateField(
        required=False,
        label='',
        help_text='Дата Рождения',
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Введите День Вашего Рождения'})
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите Email'}))

    class Meta:
        model = CastomUser

        fields = ['username', 'first_name', 'two_name', 'last_name', 'birthday', 'email', ]


class UpadatePassowordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))

    new_password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Потвердите новый пароль'}))

    class Meta:
        fields = ['new_password1', 'new_password2']
