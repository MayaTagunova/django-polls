import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    TYPE_CHOICES = [
        ('radio', 'Single choice'),
        ('checkbox', 'Multiple choice'),
        ('text', 'Text')
    ]

    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default='radio')
    question_text = models.CharField(max_length=200)


    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
