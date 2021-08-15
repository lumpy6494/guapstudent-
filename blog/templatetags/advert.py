from django import template
from blog.models import Advert

register = template.Library()


# @register.inclusion_tag('blog/advert.html')
# def show_advert():
#     adverts = Advert.objects.filter(is_published=True).order_by('-created_at')[0]
#     return {'adverts': adverts}

@register.inclusion_tag('blog/advert.html')
def show_advert():
    if (Advert.objects.exists()):
        adverts = Advert.objects.filter(is_published=True).order_by('-created_at')[0]
    else:
        adverts = ''
    return {'adverts': adverts}