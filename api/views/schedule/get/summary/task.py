"""
    Returns the specified task's basic summary 
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from django.core.exceptions import ValidationError
from api.models import Task, TimeAllotment
from django.utils import timezone


class RequestForm(forms.Form):
    task_id = forms.IntegerField()


class ResponseForm(forms.Form):
    title = forms.CharField()
    completion_assumed = forms.BooleanField()
    completed = forms.BooleanField()
    priority = forms.IntegerField()


class TaskView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        task = Task.objects.filter(id=req['task_id'], parent_goal__user=request.user).all()
        if len(task) == 0:
            raise ValidationError('Invalid task_id')
        task = task[0]

        if not task.completed:
            # Determine if completion may be assumed
            total_time_completed_m = 0

            for ta in TimeAllotment.objects.filter(task=task, end_time__lte=timezone.now()):
                total_time_completed_m += ta.duration_m()

            if total_time_completed_m >= task.total_time_required_m:
                res['completion_assumed'] = True
                if not task.completion_verification_required:
                    task.completed = True
                    task.save()

        # Set response
        res['title'] = task.title
        res['priority'] = task.priority
        res['completed'] = task.completed
