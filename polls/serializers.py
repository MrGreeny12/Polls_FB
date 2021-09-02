import datetime
from rest_framework import serializers
from polls.fields import ObjectIDField
from polls.models import Choice, Question, Poll, Answer, PollSession


class ChoiceSerializer(serializers.ModelSerializer):
    """
    Сериалайзер варианта ответа.
    """
    class Meta:
        model = Choice
        fields = ('id', 'text')
        read_only_fields = ('id', )


class QuestionDetailSerializer(serializers.ModelSerializer):
    """
    Сериалайзер вопроса.
    """
    type = serializers.ChoiceField(
        choices=Question.Type.choices,
        default=Question.Type.TEXT
    )
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'text', 'type', 'choices')
        read_only_fields = ('id', )
        extra_kwargs = {
            'poll': {'write_only': True}
        }

    def create_choices(self, question, choices):
        Choice.objects.bulk_create([
            Choice(question=question, **d) for d in choices
        ])

    def create(self, validated_data):
        choices = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        self.create_choices(question, choices)
        return question

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])
        instance.choices.all().delete()
        self.create_choices(instance, choices)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionsListSerializer(serializers.ModelSerializer):
    """
    Сериалайзер списка вопросов.
    """
    class Meta:
        model = Question
        fields = ('id', 'poll', 'text')


class PollDetailSerializer(serializers.ModelSerializer):
    """
    Сериалайзер опроса.
    """
    questions = QuestionDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = '__all__'
        read_only_fields = ('id', )

    def validate_start_date(self, value):
        """
        Отправляет ошибку, если есть попытка изменить стартовую дату после начала опроса.
        """
        if self.instance and self.instance.start_date < value:
            raise serializers.ValidationError(
                "Нельзя изменять дату, если опрос уже запущен"
            )

        return value


class PollsListSerializer(serializers.ModelSerializer):
    """
    Сериалайзер списка опросов.
    """
    class Meta:
        model = Poll
        fields = ('id', 'title', 'start_date')


class AnswerSerializer(serializers.ModelSerializer):
    """
    Сериалайзер варианта ответа в опросной сессии.
    """
    choice = ChoiceSerializer(read_only=True)
    choice_id = ObjectIDField(queryset=Choice.objects.all(), write_only=True)

    question = QuestionDetailSerializer(read_only=True)
    question_id = ObjectIDField(queryset=Question.objects.all(), write_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'question', 'choice_id', 'choice', 'value')
        read_only_fields = ('id', )


class PollSessionSerializer(serializers.ModelSerializer):
    """
    Сериалайзер опросной сессии.
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    answers = serializers.StringRelatedField(many=True)
    poll = PollDetailSerializer(read_only=True)
    poll_id = ObjectIDField(
        queryset=Poll.objects.filter(end_date__gte=datetime.date.today()),
        write_only=True
    )

    class Meta:
        model = PollSession
        fields = ('id', 'poll_id', 'poll', 'user', 'date', 'answers')
        read_only_fields = ('id', 'user', 'date')

    def create(self, validated_data):
        answers = validated_data.pop('answers', [])
        instance = PollSession.objects.create(**validated_data)
        Answer.objects.bulk_create([
            Answer(poll_session=instance, **a) for a in answers
        ])
        return instance