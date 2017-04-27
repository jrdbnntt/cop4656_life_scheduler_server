"""
    Returns the specified goal's basic summary 
"""
from django import forms
from jrdbnntt_com.views.generic import ApiView
from jrdbnntt_com.util import acl
from django.core.exceptions import ValidationError
from api.models import Goal, Task
from queue import Queue


class RequestForm(forms.Form):
    goal_id = forms.IntegerField()


class ResponseForm(forms.Form):
    title = forms.CharField()
    completed = forms.BooleanField()
    total_child_tasks = forms.IntegerField()
    total_child_tasks_completed = forms.IntegerField()


class GoalView(ApiView):
    request_form_class = RequestForm
    response_form_class = ResponseForm
    access_manager = acl.AccessManager(acl_accept=[acl.groups.USER])

    def work(self, request, req: dict, res: dict):
        goal = Goal.objects.filter(id=req['goal_id'], user=request.user).all()
        if len(goal) == 0:
            raise ValidationError('Invalid goal_id')
        goal = goal[0]

        # Breadth-first sum of child goals' tasks
        total_child_tasks = 0
        total_child_tasks_completed = 0
        goal_q = Queue()
        goal_q.put(goal)

        while not goal_q.empty():
            curr_goal = goal_q.get()

            # Add counts for this goal
            tasks = Task.objects.filter(parent_goal=curr_goal)
            total_child_tasks += tasks.count()
            total_child_tasks_completed += tasks.filter(completed=True).count()

            # Add any sub goals to queue
            for new_goal in Goal.objects.filter(parent_goal=curr_goal).all():
                goal_q.put(new_goal)

        # Make sure completed is accurate
        completed = total_child_tasks == 0 or total_child_tasks_completed /total_child_tasks == 1
        if goal.completed is not completed:
            goal.completed = completed
            goal.save()

        # Set response
        res['title'] = goal.title
        res['completed'] = completed
        res['total_child_tasks'] = total_child_tasks
        res['total_child_tasks_completed'] = total_child_tasks_completed

