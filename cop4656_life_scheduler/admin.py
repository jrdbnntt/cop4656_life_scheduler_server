from django.contrib.admin import AdminSite
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin


class LifeSchedulerAdminSite(AdminSite):
    site_header = 'Life Scheduler Administration'
    site_title = 'Life Scheduler Django Admin Panel'
    index_title = 'Home'
    site_url = '/'


site_admin = LifeSchedulerAdminSite(name='life_scheduler_admin')
site_admin.register(User, UserAdmin)
site_admin.register(Group, GroupAdmin)


