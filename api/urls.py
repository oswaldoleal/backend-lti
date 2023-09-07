from api import views
from django.urls import path

urlpatterns = [
    path('assignments', views.AssignmentsView.as_view(), name="assignments"),
    path('assignments/<int:id>/stats', views.AssignmentStatsView.as_view(), name="assignments"),
    path('games', views.GamesView.as_view(), name='games'),
    path('test', views.TestView.as_view(), name='test'),
    path('login', views.LoginView.as_view(), name='login'),
    # TODO: 'question' may not be the best name for this path
    path('question', views.QuestionsView.as_view(), name='question'),
    path('question-bank', views.QuestionBankView.as_view(), name='question-bank'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('run', views.RunView.as_view(), name='run'),
    path('score', views.ScoreView.as_view(), name='score'),
    path('user-config', views.UserConfigView.as_view(), name="user-config"),
]
