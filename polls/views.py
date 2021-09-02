from rest_framework import viewsets, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PollSessionFilter
from .serializers import PollDetailSerializer, QuestionDetailSerializer, PollsListSerializer, QuestionsListSerializer, \
    PollSessionSerializer
from .models import Poll, Question, PollSession


class PollSessionViewSet(viewsets.ModelViewSet):
    """
    REST API для сессии опроса.
    """
    queryset = PollSession.objects.all()
    serializer_class = PollSessionSerializer
    filter_backends = (DjangoFilterBackend, )
    http_method_names = ('get', 'post')
    filterset_class = PollSessionFilter

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            return serializer.save(user=self.request.user)

        return super().perform_create(serializer)


class PollCreateView(generics.CreateAPIView):
    '''
    API для создания опроса
    '''
    serializer_class = PollDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class PollsListView(generics.ListAPIView):
    '''
    API для списка опросов
    '''
    serializer_class = PollsListSerializer
    queryset = Poll.objects.all()


class PollDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API для изменения и удаления опроса
    '''
    serializer_class = PollDetailSerializer
    queryset = Poll.objects.all()
    permission_classes = [permissions.IsAdminUser]


class QuestionCreateView(generics.CreateAPIView):
    '''
    API для создания вопроса
    '''
    serializer_class = QuestionDetailSerializer
    permission_classes = [permissions.IsAdminUser]


class QuestionsListView(generics.ListAPIView):
    '''
    API для списка вопросов
    '''
    serializer_class = QuestionsListSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]


class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    API для изменения и удаления вопроса
    '''
    serializer_class = QuestionDetailSerializer
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]