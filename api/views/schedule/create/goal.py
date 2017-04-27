"""
    Creates the specified goal
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import Goal
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=1000, required=False)
    parent_goal_id = forms.IntegerField(required=False)
    default_location = forms.CharField(max_length=500, required=False)
    default_priority = forms.IntegerField(min_value=0, required=False)


class ResponseForm(forms.Form):
    goal_id = forms.IntegerField()


class GoalView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        parent_goal = None
        if req['parent_goal_id'] is not None:
            parent_goal = Goal.objects.filter(id=req['parent_goal_id'], user=request.user).all()
            if len(parent_goal) == 0:
                raise ValidationError('Invalid parent_goal_id')
            parent_goal = parent_goal[0]

        goal = Goal.objects.create(
            parent_goal=parent_goal,
            user=request.user,
            title=req['title'],
            description=req['description'],
            default_location=req['default_location'],
            default_priority=req['default_priority']
        )

        res['goal_id'] = goal.id
