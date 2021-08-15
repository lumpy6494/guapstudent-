from django import template
from datetime import datetime

from django.db.models import Q

from user.models import CastomUser

register = template.Library()


@register.inclusion_tag('blog/birthday_tpl.html')
def birthday():
    today = datetime.now().date()
    today_day=today.day
    today_month = today.month
    birthday_user = CastomUser.objects.filter(Q(birthday__day=today_day)& Q(birthday__month = today_month))
    return {'birthday_user': birthday_user}
