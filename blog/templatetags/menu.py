from django import template
from django.db.models import Count

from blog.models import Course


register = template.Library()

@register.inclusion_tag('blog/menu_tpl.html')
def show_menu(slug):
    courses = Course.objects.filter(posts__is_published = True).annotate(cnt = Count('posts')).filter(cnt__gt=0,).order_by('created_at')
    slug_url = slug.rsplit(sep='/', maxsplit=2)
    active = 'colorlib-active'
    return {'courses': courses, 'active': active,'slug_url': slug_url[1]}


