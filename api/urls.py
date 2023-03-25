from api import views
from django.urls import path


urlpatterns = [
    path('assignments', views.AssignmentsView.as_view(), name="assignments"),
    path('games', views.GamesView.as_view(), name='games'),
    path('test', views.TestView.as_view(), name='test'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('user-config', views.UserConfigView.as_view(), name="user-config"),
]
