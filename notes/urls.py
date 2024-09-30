
from django.urls import path

from notes import views

from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns=[
    path('register/',views.UserCreationView.as_view()),
    path('task/',views.TaskListCreateView.as_view()),
    path('task/<int:pk>/',views.TaskRetrieveUpdateDestroyView.as_view()),
    path('tasks/summary/', views.TaskSummaryApiView.as_view()),
    path('tasks/categories/', views.CategorieListView.as_view()),
    path('token/',ObtainAuthToken.as_view()),
]