from django.urls import path
from .views import *

urlpatterns = [
    path('account/register/activate/<str:sign>', user_activate, name = 'register_activate'),
    path('account/register/', RegisterView.as_view(), name='register'),
    path('account/register/done/', RegisterViewDone.as_view(), name='register_done'),
    path('account/login/', LoginUser.as_view(), name='login'),
    path('account/logout/', LogoutUser.as_view(), name='logout'),
    path('account/profile/', EditProfile.as_view(), name='profile'),
    path('account/profile/editpass/', EditPassword.as_view(), name='editpass'),

]
