"""
    Creates the specified goal
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl


class RequestForm(forms.Form):
    pass


class ResponseForm(forms.Form):
    pass


class GoalView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        pass
