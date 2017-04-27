"""
    Returns the tasks and goals necessary to complete the given goal. If no goal is specified, the top-level
    goals are returned.
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from jrdbnntt_com.util.forms import JsonField
from api.models import Goal, Task
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    parent_goal_id = forms.IntegerField(required=False)


class ResponseForm(forms.Form):
    goal_ids = JsonField()      # List of integer ids
    task_ids = JsonField()      # List of integer ids


class GoalRequirementsView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        task_ids = []
        goal_ids = []

        if req['parent_goal_id'] is None:
            # Return top-level goals
            for goal in Goal.objects.filter(user=request.user, parent_goal__isnull=True):
                goal_ids.append(goal.id)
        else:
            # Return goals & tasks from parent goal
            parent_goal = Goal.objects.filter(id=req['parent_goal_id'], user=request.user).all()
            if len(parent_goal) == 0:
                raise ValidationError('Invalid parent_goal_id')
            parent_goal = parent_goal[0]

            for goal in Goal.objects.filter(parent_goal=parent_goal):
                goal_ids.append(goal.id)
            for task in Task.objects.filter(parent_goal=parent_goal):
                task_ids.append(task.id)

        res['goal_ids'] = goal_ids
        res['task_ids'] = task_ids
