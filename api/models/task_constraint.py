from django.db import models
from django.contrib import admin
from cop4656_life_scheduler.admin import site_admin
from django.contrib.postgres.fields import JSONField
from api.models import Task


class TaskConstraint(models.Model):
    """ Constraints taken into consideration when creating Time Allotments (TAs) for a given task """

    class Type(object):
        MIN_TA_INTERVAL_DURATION_M = 0          # Minimum amount of time per TA
        MAX_TA_INTERVAL_DURATION_M = 1          # Maximum amount of time per TA
        DAY_RESTRICTION = 2                     # May only occur within the given day restriction settings
        REOCCURRING = 4                         # TAs are continuously created for the task, possibly forever
        TASK_DEPENDENCY = 5                     # All TAs must start after a given Task is scheduled to be completed
        EARLIEST_START_TIME = 6                 # All TAs must start after this datetime
        LATEST_END_TIME = 7                     # All TAs must end before this datetime

        choices = (
            (MIN_TA_INTERVAL_DURATION_M, 'Min TA Interval Duration (m)'),
            (MAX_TA_INTERVAL_DURATION_M, 'Max TA Interval Duration (m)'),
            (DAY_RESTRICTION, 'Day Restriction'),
            (REOCCURRING, 'Reoccurring'),
            (TASK_DEPENDENCY, 'Task Dependency'),
            (EARLIEST_START_TIME, 'Earliest Start Time'),
            (LATEST_END_TIME, 'Latest End Time')
        )

    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
    constraint_type = models.PositiveSmallIntegerField(choices=Type.choices)
    settings = JSONField()

    def __str__(self) -> str:
        return '[{}]'.format(self.__class__.__name__)


@admin.register(TaskConstraint, site=site_admin)
class TaskConstraintAdmin(admin.ModelAdmin):
    list_filter = ('constraint_type',)
    list_display = ('id', 'task', 'constraint_type')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ()
    ordering = ('-task__id', 'constraint_type')
