from django.shortcuts import render
# Create your views here.
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django import forms
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.urls import reverse

from .models import Discussion, Comment



def discussion(request):
    context = {
        'discussion': Discussion.objects.all()
    }
    return render(request, 'discussion/discussion_list.html', context)


# All Forms
class DiscussionCreateForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields =['title', 'content']


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


# All Views
class DiscussionMainView(ListView):
    model = Discussion
    template_name = 'discussion/discussion_list.html'
    context_object_name = 'discussion'
    ordering = ['-date_posted']


class DiscussionDetailView(FormMixin, DetailView):
    model = Discussion
    template_name = 'discussion/discussion_detail.html'
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super(DiscussionDetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.all()
        context['form'] = CommentCreateForm(initial={'discussion': self.object})
        return context

    def get_success_url(self):
        return reverse('discussion_detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.discussion = self.object
        form.instance.commenter = self.request.user.developer
        form.save()
        return super(DiscussionDetailView, self).form_valid(form)


class DiscussionCreateView(SuccessMessageMixin, CreateView):
    model = Discussion
    template_name = 'discussion/discussion_form.html'
    fields = ['title', 'content']
    success_message = "Your discussion has been successfully created."
    
    def form_valid(self,form):
        form.instance.author = self.request.user.developer
        return super().form_valid(form)


def add_comment_to_discussion(request,pk):
        discussion = get_object_or_404(Discussion,pk=pk)
        if request.method == 'POST':
            form = CommentCreateForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                # comment.post = post
                comment.commenter = request.user
                comment.save()
                
        else:
            form = CommentCreateForm()
        return render(request, 'discussion/comment_success.html', {'form': form})






