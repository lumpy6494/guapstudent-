from django.db.models import F, Q
from django.views.generic import ListView, DetailView, CreateView
from .models import Course, Post, Tag, Subject, Advert, CloudService, ViewsUser, Birthday
from .forms import PostForm


class Home(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class PostByCourse(ListView):
    template_name = 'blog/course.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.filter(is_published=True, courses__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(PostByCourse, self).get_context_data(**kwargs)
        context['title'] = 'Новости по курсу: '+ str(Course.objects.get(slug=self.kwargs['slug']))
        return context


class PostBySubject(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 7
    allow_empty = False


    def get_queryset(self):
        return Post.objects.filter(is_published=True, subjects__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(PostBySubject, self).get_context_data(**kwargs)
        context['title'] = 'Новости по предмету: '+ str(Subject.objects.get(slug=self.kwargs['slug']))
        return context


class AdvertView(DetailView):
    model = Advert
    context_object_name = 'adverts'
    template_name = 'blog/advert.html'


class BirthdayView(DetailView):
    model = Birthday
    context_object_name = 'birthday'
    template_name = 'blog/birthday_tpl.html'


class PostByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 7


    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Записи по тегу : ' + str(Tag.objects.get(slug=self.kwargs['slug']))
        return context


class ViewPost(DetailView):
    model = Post
    template_name = 'blog/viewpost.html'
    context_object_name = 'post'

    def setup(self, request, *args, **kwargs):
        context = super(ViewPost, self).setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            self.uuid_user = self.request.user.uuid
            self.first_name = self.request.user.first_name
            self.two_name = self.request.user.two_name
            self.last_name = self.request.user.last_name
            self.obj, self.created = ViewsUser.objects.update_or_create(
                uuid_us = self.uuid_user,
                first_name_user=self.first_name,
                two_name_user = self.two_name,
                last_name_user=self.last_name
            )
        return context

    def get_context_data(self, **kwargs):
        context = super(ViewPost, self).get_context_data(**kwargs)

        try:
            if not self.object in self.obj.views_users.all():
                self.object.views = F('views') + 1

            if self.obj:
                self.obj.views_users.add(self.object)

            self.object.save()
            self.object.refresh_from_db()

        except AttributeError:
            pass

        return context


class Search(ListView):
    template_name = 'blog/search.html'
    context_object_name = 'posts'
    paginate_by = 7

    def get_queryset(self):
        return Post.objects.filter(
            Q(content__icontains=self.request.GET.get('s')) | Q(title__icontains=self.request.GET.get('s')))

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
