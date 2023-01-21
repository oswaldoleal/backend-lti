from api import views
from django.urls import path


urlpatterns = [
    path('test', views.TestView.as_view(), name='test'),
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('user-config', views.UserConfigView.as_view(), name="user-config"),
]
