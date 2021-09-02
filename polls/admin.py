from django.contrib import admin
from polls.models import Poll, Question, Choice

admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Choice)
