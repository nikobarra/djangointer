from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("signout/", views.signout, name="signout"),
    path("tasks/", views.tasks, name="tasks"),
    path("signin/", views.signin, name="signin"),
    path("create_task/", views.create_task, name="create_task"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/complete", views.task_complete, name="task_complete"),
    path("tasks/<int:task_id>/delete", views.task_delete, name="task_delete"),
    path("tasks_completed/", views.tasks_completed, name="tasks_completed"),
]
