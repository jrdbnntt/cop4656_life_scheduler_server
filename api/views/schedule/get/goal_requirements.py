"""
    Returns the tasks and goals necessary to complete the given goal. If no goal is specified, the top-level
    goals are returned.
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl


class RequestForm(forms.Form):
    pass


class ResponseForm(forms.Form):
    pass


class GoalRequirementsView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        pass
