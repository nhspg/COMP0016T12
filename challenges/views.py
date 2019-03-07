from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Developer
from .models import Challenge
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.
from .models import Challenge
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

def createChallenge(request):
    context = {
        'challenges': Challenge.objects.all()
    }
    return render(request, 'challenges/challenge_list.html', context)


def user_is_participating(challengeid, userid):
    current_challenge = Challenge.objects.get(pk=challengeid)
    for devs in current_challenge.developers.all():
        if devs.pk == userid:
            return True
    return False

def participateInChallenge(request, challengeid):
    user = Developer.objects.get(user=request.user)
    if not user_is_participating(challengeid, user.pk):
        Challenge.objects.get(pk=challengeid).developers.add(user)
        # return render(request, 'challenges/challenge_list.html')
    return HttpResponseRedirect(reverse('challenges_detail', args=[challengeid]))


def leaveChallenge(request, challengeid):
    user = Developer.objects.get(user=request.user)
    if user_is_participating(challengeid, user.pk):
        Challenge.objects.get(pk = challengeid).developers.remove(user)
        # return render(request, 'challenges/challenge_list.html')
    return HttpResponseRedirect(reverse('challenges_detail', args=[challengeid]))


class ChallengeMainView(ListView):
    model = Challenge
    template_name = 'challenges/challenge_list.html'
    context_object_name = 'challenges'
    ordering = ['-date_created']

class ChallengeOverviewView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_overview.html'

class ChallengeDataView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_data.html'

class ChallengeSolutionsView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_solutions.html'

class ChallengeDiscussionView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_discussion.html'

class ChallengeLeaderboardView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_leaderboard.html'

class ChallengeRulesView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_rules.html'


class ChallengeCreateView(SuccessMessageMixin, CreateView):
    model = Challenge
    fields = ['title',  'award', 'description', 'data', 'evaluation', 'timeline', 'rule', 'brief']
    success_message = "The challenge has been successfully created."

    def form_valid(self, form):
        form.instance.clinician = self.request.user.clinician
        form.save()
        return super(ChallengeCreateView, self).form_valid(form)


class ChallengeUpdateView(SuccessMessageMixin, UserPassesTestMixin, UpdateView):
    model = Challenge
    fields = ['title',  'award', 'description', 'data', 'evaluation', 'timeline', 'rule', 'brief']
    success_message = "The challenge has been successfully updated."

    def form_valid(self, form):
        form.instance.clinician = self.request.user.clinician
        return super(ChallengeUpdateView, self).form_valid(form)

    def test_func(self):
        challenge = self.get_object()
        if self.request.user.clinician == challenge.clinician:
            return True
        return False


class ChallengeDeleteView(UserPassesTestMixin, DeleteView):
    model = Challenge
    success_url = '/'
    success_message = 'The challenge has been successfully deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ChallengeDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        challenge = self.get_object()
        if self.request.user.clinician == challenge.clinician:
            return True
        return False