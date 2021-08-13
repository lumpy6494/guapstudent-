from django import template
from django.db.models import Count

from blog.models import Subject


register = template.Library()

@register.inclusion_tag('blog/subject_tpl.html')
def show_subject():
    subjects = Subject.objects.filter(posts__is_published = True).annotate(cnt = Count('posts'))
    # [:7]
    return {'subjects': subjects}


@register.inclusion_tag('blog/subject_tpl.html')
def show_subject_one(slug_url):
    slug_url = slug_url.rsplit(sep='/', maxsplit=2)
    subjects = Subject.objects.filter(posts__is_published = True, course_sub__slug= slug_url[1]).annotate(cnt=Count('posts'))
    return {'subjects': subjects}

