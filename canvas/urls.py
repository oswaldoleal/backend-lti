from canvas import views
from django.urls import path


urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('launch', views.LaunchView.as_view(), name='launch'),
]
