from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'user/login$', views.user.LogInView.as_view()),
    url(r'user/logout$', views.user.LogOutView.as_view()),
    url(r'user/register$', views.user.RegisterView.as_view()),
    url(r'user/get/summary$', views.user.get.SummaryView.as_view())
]
