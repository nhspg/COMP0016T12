from django.shortcuts import render
# Create your views here.
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django import forms
from .models import Solution
from .models import Challenge
from challenges.templatetags import template_methods
from django.http import HttpResponse


def solution(request):
    context = {
        'solutions': Solution.objects.all()
    }
    return render(request, 'solutions/solution_list.html', context)


class SolutionMainView(ListView):
    model = Solution
    template_name = 'solutions/solution_list.html'
    context_object_name = 'solutions'
    ordering = ['-date_created']


class SolutionDetailView(DetailView):
    model = Solution


class SolutionForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=['title', 'description', 'challenge', 'solution_data']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(SolutionForm, self).__init__(*args, **kwargs)
        self.fields['challenge'].queryset = user.developer.challenge_set.all()


class SolutionEvaluationForm(forms.ModelForm):
    class Meta:
        model=Solution
        fields=['title', 'description', 'challenge', 'solution_data', 'accuracy']

    def __init__(self, *args, **kwargs):
        super(SolutionEvaluationForm, self).__init__(*args, **kwargs)
        self.fields['title'].disabled = True
        self.fields['description'].disabled = True
        self.fields['challenge'].disabled = True
        self.fields['solution_data'].disabled = True

class SolutionCreateView(CreateView):
    template_name = 'solutions/solution_form.html'
    form_class = SolutionForm

    def get_form_kwargs(self):
        kwargs = super(SolutionCreateView, self).get_form_kwargs()
        kwargs ['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.developer = self.request.user.developer
        form.save()
        return super(SolutionCreateView, self).form_valid(form)


class SolutionSpecCreateView(CreateView):
    model = Solution
    fields = ['title', 'description', 'solution_data']

    def form_valid(self, form):
        form.instance.developer = self.request.user.developer
        form.instance.challenge = Challenge.objects.get(pk=self.kwargs['challengepk'])
        if template_methods.user_is_in_challenge(self.kwargs['challengepk'], self.request.user.developer.id):
            form.save()
            return super(SolutionSpecCreateView, self).form_valid(form)
        else: return HttpResponse('<h1>You have not yet participated in that challenge</h1>')


class SolutionUpdateView(UserPassesTestMixin, UpdateView):
    model = Solution
    fields = ['title', 'description', 'solution_data']

    def form_valid(self, form):
        form.instance.developer = self.request.user.developer
        return super(SolutionUpdateView, self).form_valid(form)

    def test_func(self):
        solution = self.get_object()
        if self.request.user.developer == solution.developer:
            return True
        return False


class SolutionEvaluateView(UserPassesTestMixin, UpdateView):
    model = Solution
    template_name_suffix = "_evaluate_form"
    form_class = SolutionEvaluationForm

    def test_func(self):
        solution = self.get_object()
        if self.request.user.clinician == solution.challenge.clinician:
            return True
        return False


class SolutionDeleteView(UserPassesTestMixin, DeleteView):
    model = Solution
    success_url = '/'

    def test_func(self):
        solution = self.get_object()
        if self.request.user.developer == solution.developer:
            return True
        return False