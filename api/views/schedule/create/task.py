"""
    Creates the specified task
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import Goal, Task, TimeAllotment
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    parent_goal_id = forms.IntegerField()
    task_type = forms.ChoiceField(choices=Task.Type.choices)
    title = forms.CharField(max_length=100)
    priority = forms.IntegerField(min_value=0)
    total_time_required_m = forms.IntegerField(min_value=0)
    completion_verification_required = forms.BooleanField(required=False)
    description = forms.CharField(max_length=1000, required=False)
    location = forms.CharField(max_length=500, required=False)
    fixed_time_allotment_start = forms.DateTimeField(required=False)
    fixed_time_allotment_end = forms.DateTimeField(required=False)


class ResponseForm(forms.Form):
    task_id = forms.IntegerField()


class TaskView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        parent_goal = Goal.objects.filter(id=req['parent_goal_id'], user=request.user).all()
        if len(parent_goal) == 0:
            raise ValidationError('Invalid parent_goal_id')
        parent_goal = parent_goal[0]

        if req['task_type'] is Task.Type.FIXED_EVENT \
                and (req['fixed_time_allotment_start'] is None or req['fixed_time_allotment_end'] is None):
            raise ValidationError('Missing fixed_time_allotment for Fixed Event')

        task = Task(
            parent_goal=parent_goal,
            task_type=req['task_type'],
            title=req['title'],
            description=req['description'],
            priority=req['priority'],
            total_time_required_m=req['total_time_required_m'],
            completion_verification_required=req['completion_verification_required'],
            location=req['location'] if req['location'] is not None else parent_goal.get_default_location()

        )
        res['task_id'] = task.id

        if task.Type is Task.Type.FIXED_EVENT:
            TimeAllotment.objects.create(
                task=task,
                start_time=req['fixed_time_allotment_start'],
                end_time=req['fixed_time_allotment_end']
            )

