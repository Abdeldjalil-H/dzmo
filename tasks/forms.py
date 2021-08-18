from django.forms import ModelForm
from django import forms
from .models import TaskComment, TaskProblemSubmission, Task
from control.forms import AddProblemsForm
from problems.forms import CommentForm, SubmitForm

class SubmitForm(SubmitForm):
    class Meta(SubmitForm.Meta):
        model = TaskProblemSubmission

class CommentForm(CommentForm):
    class Meta(CommentForm.Meta):
        model = TaskComment

LEVELS = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]

class AddProblemsForm(forms.Form):
  
    statements  = forms.CharField(widget=forms.Textarea(),label ='المسائل')
    task = forms.ModelChoiceField(queryset=Task.objects.all(), label='الواجب')  
    level       = forms.ChoiceField(choices = LEVELS, label = 'المستوى')
