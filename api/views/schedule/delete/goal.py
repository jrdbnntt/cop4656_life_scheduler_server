"""
    Deletes the specified goal and implicitly delete all of its tasks, goals, and any of their time allotments 
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import Goal
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    goal_id = forms.IntegerField()


class GoalView(ApiView):
    request_form_class = RequestForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        goal = Goal.objects.filter(id=req['goal_id'], user=request.user).all()
        if len(goal) == 0:
            raise ValidationError('Invalid goal_id')
        goal.delete()
