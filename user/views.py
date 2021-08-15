from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

from blog.models import Post, ViewsUser
from user.forms import RegisterForm, UserLoginForm, UpadateUserForm, UpadatePassowordForm

from user.models import CastomUser, Promokod


class LoginUser(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm


class LogoutUser(LogoutView):
    template_name = 'user/logout.html'
    success_url = reverse_lazy('logout')


class RegisterView(CreateView):
    model = CastomUser
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def get_queryset(self):
        return Promokod.objects.all()

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        promo = form.cleaned_data['promo']
        promokod = self.get_queryset()
        user = form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        for item in promokod:
            if str(item) == str(promo):
                group = Group.objects.get(name='Студент')
                user.groups.add(group)
                group.save()

        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class EditProfile(LoginRequiredMixin, UpdateView):
    model = CastomUser
    template_name = 'user/profile.html'
    form_class = UpadateUserForm
    success_url = reverse_lazy('profile')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class EditPassword(LoginRequiredMixin, PasswordChangeView):
    form_class = UpadatePassowordForm
    template_name = 'user/editpass.html'
    success_url = reverse_lazy('profile')




# Срач в коде :D
# def register_user(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             promo = form.cleaned_data['promo']
#             promokod = Promokod.objects.all()
#             user = form.save()
#             for item in promokod:
#                 if str(item) == str(promo):
#                     group = Group.objects.get(name='Студент')
#                     user.groups.add(group)
#                     group.save()
#                     login(request, user)
#             messages.success(request, 'Успешно!')
#             return redirect('home')
#         else:
#             messages.error(request, "Ошибка")
#     else:
#         form = RegisterForm()
#     return render(request, 'user/register.html', {'form':form})


# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data = request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserLoginForm()
#
#     return render(request, 'user/login.html', {'form':form})


# def user_logout(request):
#     logout(request)
#     return redirect('login')
