from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from cop4656_life_scheduler.admin import site_admin


class ExtendedUserInfo(models.Model):
    """ Extended User information """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return '[{} {}]'.format(self.__class__.__name__, self.user.username)


@admin.register(ExtendedUserInfo, site=site_admin)
class ExtendedUserInfoAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('id', 'user')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    ordering = ('-user__date_joined',)
