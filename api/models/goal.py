from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from cop4656_life_scheduler.admin import site_admin


class Goal(models.Model):
    """
        A complicated desire of the user that they may attempt to accomplish by a set of specific tasks.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, default='')

    parent_goal = models.ForeignKey(to='self', on_delete=models.CASCADE, null=True, blank=True)

    default_location = models.CharField(max_length=500, default='')
    default_priority = models.PositiveIntegerField(null=True, blank=True)

    # This is purely a stored calculation of the status of the Goal's Tasks. Must be updated if Tasks are altered
    completed = models.BooleanField(default=False)

    def get_default(self, attribute: str):
        source = self
        while True:
            value = getattr(source, attribute, None)
            if value is not None:
                return value
            if source.parent_goal is None:
                break
            else:
                source = source.parent_goal
        return None

    def get_default_location(self):
        return self.get_default('default_location')

    def get_default_priority(self):
        return self.get_default('default_priority')

    def __str__(self) -> str:
        return '[{} {}]'.format(self.__class__.__name__, self.title)


@admin.register(Goal, site=site_admin)
class GoalAdmin(admin.ModelAdmin):
    list_filter = ()
    list_display = ('id', 'user', 'title')
    list_editable = ()
    list_display_links = ('id',)
    search_fields = (
        'title', 'description',
        'user__email', 'user__first_name', 'user__last_name'
    )
    ordering = ('-created_at',)
