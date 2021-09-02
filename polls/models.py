import datetime
from django.contrib.auth import get_user_model
from django.db import models


class Poll(models.Model):
    '''
    Модель опроса.
    '''
    title = models.CharField(max_length=256, verbose_name='Название')
    start_date = models.DateField(
        default=datetime.date.today,
        editable=False,
        verbose_name='Дата начала'
    )
    end_date = models.DateField(
        default=datetime.date.today,
        editable=True,
        verbose_name='Дата окончания'
    )
    description = models.TextField(
        max_length=1024,
        verbose_name='Описание опроса',
        help_text='Аннотация к опросу'
    )

    def __str__(self):
        return self.title


class Question(models.Model):
    '''
    Модель вопроса. В одном опросе может быть несколько
    вопросов.
    '''
    class Type:
        TEXT = 'TEXT'
        CHOICE = 'CHOICE'
        MULTICHOICE = 'MULTICHOICE'

        choices = (
            (TEXT, 'TEXT'),
            (CHOICE, 'CHOICE'),
            (MULTICHOICE, 'MULTICHOICE'),
        )

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name='Опрос'
    )
    text = models.CharField(
        max_length=256,
        verbose_name='Содержание',
        help_text='Введите вопрос'
    )
    type = models.CharField(
        max_length=16,
        choices=Type.choices,
        default=Type.TEXT,
        verbose_name='Тип вопроса'
    )

    def __str__(self):
        return self.text


class Choice(models.Model):
    '''
    Модель варианта ответа. У одного вопроса может быть несколько
    вариантов ответа.
    '''
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        related_name='choices',
    )
    text = models.CharField(
        max_length=64,
        verbose_name='Содержание',
        help_text='Введите вариант ответа'
    )


class PollSession(models.Model):
    '''
    Модель сессии опроса, которая привязана к определённому пользователю
    '''
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        verbose_name='Опрос'
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        blank=True,
        null=True
    )
    date = models.DateField(default=datetime.date.today, editable=False)


class Answer(models.Model):
    '''
    Модель результата ответа на определенный вопрос
    '''
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос'
    )
    poll_session = models.ForeignKey(
        PollSession,
        on_delete=models.CASCADE,
        verbose_name='Опросная сессия',
        related_name='answers'
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        verbose_name='Вариант ответа'
    )
    value = models.CharField(max_length=128, blank=True, null=True)