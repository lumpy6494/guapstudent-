from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('course/<str:slug>/', PostByCourse.as_view(), name='course'),
    path('subject/<str:slug>/', PostBySubject.as_view(), name='subject'),
    path('tag/<str:slug>/', PostByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
    path('add_post/', AddPost.as_view(), name = 'add_post'),
    path('service/', CloudServiceView.as_view(), name = 'mega'),
    path('post/<int:pk>/', ViewPost.as_view(), name='post'),

]
