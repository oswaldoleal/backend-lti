from canvas import views
from django.urls import re_path


urlpatterns = [
    re_path(r"^login/$", views.LoginView.as_view(), name="login"),
    re_path(r"^launch/$", views.LaunchView.as_view(), name="launch"),
]
