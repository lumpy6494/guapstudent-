from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.core.exceptions import ObjectDoesNotExist

from user.forms import RegisterForm, UserLoginForm, UpadateUserForm, UpadatePassowordForm
from django.core.signing import BadSignature
from user.models import CastomUser, Promokod
from .apps import user_registered
from .utilites import signer


class LoginUser(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm


class LogoutUser(LogoutView):
    template_name = 'user/logout.html'
    success_url = reverse_lazy('logout')


class RegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_done')

    def get_queryset(self):
        return Promokod.objects.all()

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        promo = form.cleaned_data['promo']
        promokod = self.get_queryset()
        user = form.save()
        for item in promokod:
            if str(item) == str(promo):
                try:
                    group = Group.objects.get(name=item.gpoup_user)
                    user.groups.add(group)
                    group.save()
                except ObjectDoesNotExist:
                    pass
        user_registered.send(RegisterForm, instance=user)
        return valid


class RegisterViewDone(TemplateView):
    template_name = 'user/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return None
    user = get_object_or_404(CastomUser, username=username)
    if user.is_activated:
        template = 'blog/index.html'
        if not user.is_authenticated:
            login(request, user)
    else:
        template = 'user/register_activate.html'
        user.is_activated = True
        user.is_active = True
        user.save()
        login(request, user)

    return render(request, template)


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
