"""
    Returns generated time allotments (aka a generated schedule)
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from jrdbnntt_com.util.forms import JsonField
from api.models import TimeAllotment
from django.utils import timezone


class RequestForm(forms.Form):
    past = forms.BooleanField(required=False)
    complete_tasks = forms.BooleanField(required=False)


class ResponseForm(forms.Form):
    time_allotments = JsonField()


class TimeAllotmentsView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        qs = TimeAllotment.objects.filter(
            task__parent_goal__user=request.user,
            task__completed=req['complete_tasks'] is True,
        )

        if req['past']:
            qs = qs.filter(end_time__lte=timezone.now())

        time_allotments = []
        for ta in qs.all():
            time_allotments.append({
                'task_id': ta.task_id,
                'task_title': ta.task.title,
                'start_time': ta.start_time.isoformat(),
                'end_time': ta.end_time.isoformat(),
                'duration': ta.duration_m()
            })

        res['time_allotments'] = time_allotments