from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'user/login$', views.user.LogInView.as_view()),
    url(r'user/logout$', views.user.LogOutView.as_view()),
    url(r'user/register$', views.user.RegisterView.as_view()),
    url(r'user/get/summary$', views.user.get.SummaryView.as_view()),

    url(r'schedule/generate$', views.schedule.GenerateView.as_view()),
    url(r'schedule/create/goal$', views.schedule.create.GoalView.as_view()),
    url(r'schedule/create/task$', views.schedule.create.TaskView.as_view()),
    url(r'schedule/delete/goal$', views.schedule.delete.GoalView.as_view()),
    url(r'schedule/delete/task$', views.schedule.delete.TaskView.as_view()),
    url(r'schedule/get/goal_requirements$', views.schedule.get.GoalRequirementsView.as_view()),
    url(r'schedule/get/time_allotments$', views.schedule.get.TimeAllotmentsView.as_view()),
    url(r'schedule/get/details/goal$', views.schedule.get.details.GoalView.as_view()),
    url(r'schedule/get/details/task$', views.schedule.get.details.TaskView.as_view()),
    url(r'schedule/get/summary/goal$', views.schedule.get.summary.GoalView.as_view()),
    url(r'schedule/get/summary/task$', views.schedule.get.summary.TaskView.as_view())
]
