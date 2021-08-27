from django import template
from django.db.models import Count

from blog.models import Tag

register = template.Library()


@register.inclusion_tag('blog/tags.html')
def show_tags():
    tags = Tag.objects.filter(posts__is_published = True).annotate(cnt = Count('posts')).filter(cnt__gt=0)
    return {'tags': tags}
