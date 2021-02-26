from django.contrib.admin import ModelAdmin, register

from .models import LoggedInUser


@register(LoggedInUser)
class LoggedInUserAdmin(ModelAdmin):
    list_display = ('user', 'logged_in_before', 'stream_link','ip')
    icon_name = 'people'
