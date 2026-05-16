from django.urls import path
from . import views


urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('assign-task/<int:task_id>/', views.assign_task, name='assign_task'),
]