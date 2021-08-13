from django.contrib.auth.models import User
from django.db.models import F, Q
from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from .models import Course, Post, Tag, Subject, Advert, CloudService
from .forms import PostForm




class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.filter(is_published = True)

class PostByCourse(ListView):
    template_name = 'blog/course.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.filter(is_published = True, courses__slug = self.kwargs['slug'])


class PostBySubject(ListView):
    template_name ='blog/index.html'
    context_object_name = 'posts'
    paginate_by = 7
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(is_published = True, subjects__slug=self.kwargs['slug'])

class ViewPost(DetailView):
    model = Post
    template_name ='blog/viewpost.html'
    context_object_name = 'post'


    def get_context_data(self, **kwargs):
        context = super(ViewPost, self).get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context




class AdvertView(DetailView):
    model = Advert
    context_object_name = 'adverts'
    template_name = 'blog/advert.html'


class PostByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 7


    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу: ' + str(Tag.objects.get(slug = self.kwargs['slug']))
        return context

class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.filter(Q(content__icontains=self.request.GET.get('s')) | Q(title__icontains=self.request.GET.get('s')) )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context

class AddPost(CreateView):
    form_class = PostForm
    template_name = 'blog/add_post.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(AddPost, self).form_valid(form)


class CloudServiceView(ListView):
    model = CloudService
    template_name = 'blog/mega.html'
    context_object_name = 'cloudservices'
    paginate_by = 7






