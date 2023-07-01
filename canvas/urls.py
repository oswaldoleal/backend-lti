from canvas import views
from django.urls import re_path, path

urlpatterns = [
    re_path(r"^login/$", views.LoginView.as_view(), name="login"),
    re_path(r"^launch/$", views.LaunchView.as_view(), name="launch"),
    # TODO: the avatar belongs on the API app, it has nothing to do with canvas
    path('avatar', views.AvatarView.as_view(), name="avatar"),
]
