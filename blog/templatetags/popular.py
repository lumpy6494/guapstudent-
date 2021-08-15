from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('blog/popular_tpl.html')
def show_popular():
    popular = Post.objects.filter(is_published=True).order_by('-views')[:3]
    return {'popular': popular}