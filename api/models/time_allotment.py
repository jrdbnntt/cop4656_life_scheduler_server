from django.db import models
from django.contrib import admin
from cop4656_life_scheduler.admin import site_admin
from api.models import Task


class TimeAllotment(models.Model):
    """
        A specified unit of time to work on a task.
        
        Start and end times are precise to the minute.
        
        A collection of these is a Calendar/Schedule. When new Calendars are generated, only TAs from incomplete
        tasks are considered, but only those in the future may be changed.
    """

    task = models.ForeignKey(to=Task, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def duration_m(self) -> int:
        return (self.end_time - self.start_time).minute

    def __str__(self) -> str:
        return '[{}]'.format(self.__class__.__name__)


@admin.register(TimeAllotment, site=site_admin)
class TimeAllotmentAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('id', 'task', 'start_time')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = ()
    ordering = ('-task__id', 'start_time')
