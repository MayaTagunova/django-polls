from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question, Poll, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'polls_list'


    def get_queryset(self):
        """Return all published polls."""
        return Poll.objects.filter(pub_date__lte=timezone.now())


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'


    def get_queryset(self):
        return Poll.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'


    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())


class UserView(generic.ListView):
    model = Poll
    template_name = 'polls/user.html'
    context_object_name = 'user_polls_list'


    def get_queryset(self):
        return Poll.objects.all()


def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)

    if not request.session.session_key:
        request.session.create()

    print(f'Session key: {request.session._session_key}')

    voted_polls = request.session.get('voted_polls', [])
    print(f'Voted polls: {voted_polls}')
    if poll_id in voted_polls:
        return render(request, 'polls/results.html', {
        'poll': poll,
        'error_message': "You have already voted on this poll.",
    })

    for question in poll.question_set.all():
        selected_choices = []
        try:
            name = f'choice{question.id}'
            if question.type == 'radio':
                selected_choices.append(question.choice_set.get(pk=request.POST[name]))
            elif question.type == 'checkbox':
                choice_ids = request.POST.getlist(name)
                for choice_id in choice_ids:
                    selected_choices.append(question.choice_set.get(pk=int(choice_id)))
            elif question.type == 'text':
                choice = Choice.objects.get_or_create(question=question, choice_text=request.POST[name])[0]
                choice.votes += 1
                choice.save()

        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'poll': poll,
                'error_message': "You haven't selected anything.",
            })

        else:
            for selected_choice in selected_choices:
                selected_choice.votes += 1
                selected_choice.save()
                Vote.objects.create(choice=selected_choice, session_key=request.session.session_key)

            voted_polls.append(poll_id)
            request.session['voted_polls'] = voted_polls


    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))


def get_queryset(self):
    """
    Return all published polls (not including those set to be
    published in the future).
    """
    return Polls.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')
