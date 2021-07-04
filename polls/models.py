import datetime

from django.db import models
from django.utils import timezone


class Poll(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


    def __str__(self):
        return self.title


    def was_published_recently(self):
        now = timezone.now()
        return now >= self.pub_date >= now - datetime.timedelta(days=1)


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
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


class Vote(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=200)

    def __str__(self):
        return f'{str(self.choice)} : {self.session_key}'
