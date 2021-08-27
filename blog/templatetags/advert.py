from django import template
from blog.models import Advert

register = template.Library()

@register.inclusion_tag('blog/advert.html')
def show_advert():
    try:
        if (Advert.objects.exists):
            adverts = Advert.objects.filter(is_published=True).order_by('-created_at')[0]
        else:
            adverts = ''
        return {'adverts': adverts}
    except IndexError:
        pass
