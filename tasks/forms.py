from django import forms
from .models import TaskComment, TaskProblemSubmission, Task, TASKS_LEVELS
from problems.forms import CommentForm, SubmitForm


class SubmitForm(SubmitForm):
    class Meta(SubmitForm.Meta):
        model = TaskProblemSubmission


class CommentForm(CommentForm):
    class Meta(CommentForm.Meta):
        model = TaskComment


class AddProblemsForm(forms.Form):
    statements = forms.CharField(widget=forms.Textarea(), label="المسائل")
    task = forms.ModelChoiceField(queryset=Task.objects.all(), label="الواجب")
    level = forms.ChoiceField(choices=TASKS_LEVELS, label="المستوى")
