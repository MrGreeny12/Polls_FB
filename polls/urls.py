from django.urls import path, include
from rest_framework.routers import DefaultRouter
from polls.views import *


router = DefaultRouter()
router.register(r'poll_session', PollSessionViewSet)


app_name = 'polls'
urlpatterns = [
    path('poll/create/', PollCreateView.as_view()),
    path('poll/list/', PollsListView.as_view()),
    path('poll/detail/<int:pk>/', PollDetailView.as_view()),
    path('question/create/', QuestionCreateView.as_view()),
    path('question/list/', QuestionsListView.as_view()),
    path('question/detail/<int:pk>/', QuestionDetailView.as_view()),
    path('', include((router.urls, 'poll_session')))
]