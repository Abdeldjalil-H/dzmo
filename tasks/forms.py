from django.db import models
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import TaskComment, TaskProblemSubmission, Task
from control.forms import AddProblemsForm
class SubmitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['solution'].required = False
    class Meta:
        model = TaskProblemSubmission
        fields = ['ltr_dir','solution','file']
        widgets = {
            'ltr_dir':forms.CheckboxInput( attrs = {'style':'position:inherit;margin-left:4px;','onclick':"change_dir('MathInput')"}),
            'solution':forms.Textarea(attrs={'id':'MathInput'})
        }
        labels = {
            'ltr_dir':'الكتابة من اليسار',
            'solution':'',
            'file':'إرفاق ملف'
        }
    ''' 
    def clean_solution(self):
        data = self.cleaned_data['solution']
        if self.files.get('file'):
            return data if data else None
        return data
    '''
    def clean(self):
        if not self.cleaned_data['solution'] and not self.cleaned_data['file']:
            raise ValidationError('يجب أن تقوم بكتابة إجابة، أو رفع ملف يحتوي على الإجابة.')
        return super().clean()

class CommentForm(ModelForm):
    class Meta:
        model  = TaskComment
        fields = ['ltr_dir', 'content']
        widgets = {
            'content': forms.Textarea(
                        attrs={'id':'MathInput',}),
            'ltr_dir': forms.CheckboxInput( attrs = {'style':'position:inherit;margin-left:4px;','onclick':"change_dir()",})       
        }
        labels = {
            'content':''
        }
LEVELS = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]

class AddProblemsForm(forms.Form):
  
    statements  = forms.CharField(widget=forms.Textarea(),label ='المسائل')
    task = forms.ModelChoiceField(queryset=Task.objects.all(), label='الواجب')  
    level       = forms.ChoiceField(choices = LEVELS, label = 'المستوى')
