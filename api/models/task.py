from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from cop4656_life_scheduler.admin import site_admin
from api.models import Goal


class Task(models.Model):

    class Type(object):
        FIXED_EVENT = 0     # Future TimeAllotments may not be rearranged automatically
        FLEXIBLE = 1        # May be split up into multiple TimeAllotments
        ONE_SHOT = 2        # May not be split up into multiple TimeAllotments

        choices = (
            (FIXED_EVENT, 'Fixed Event'),
            (FLEXIBLE, 'Flexible'),
            (ONE_SHOT, 'One-Shot')
        )

    # Identity information
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    parent_goal = models.ForeignKey(to=Goal, on_delete=models.CASCADE)
    task_type = models.PositiveSmallIntegerField(choices=Type.choices)

    # Basic information
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length=500, null=True, blank=True)

    # Scheduling information
    priority = models.PositiveIntegerField()
    total_time_required_m = models.PositiveIntegerField(null=True, blank=True)
    completion_verification_required = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return '[{} {}]'.format(self.__class__.__name__, self.title)


@admin.register(Task, site=site_admin)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('id', 'parent_goal', 'title')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = (
        'title', 'description',
        'goal__title', 'goal__description',
        'user__email', 'user__first_name', 'user__last_name'
    )
    ordering = ('-created_at',)
