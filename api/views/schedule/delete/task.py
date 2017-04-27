"""
    Deletes the specified task and implicitly delete all of its time allotments 
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from api.models import Task
from django.core.exceptions import ValidationError


class RequestForm(forms.Form):
    task_id = forms.IntegerField()


class ResponseForm(forms.Form):
    pass


class TaskView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        task = Task.objects.filter(id=req['task_id'], parent_goal__user=request.user).all()
        if len(task) == 0:
            raise ValidationError('Invalid task_id')
        task.delete()
