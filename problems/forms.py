from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import ProblemSubmission, Comment


class SubmitForm(ModelForm):

    def __init__(self, dir_attrs={}, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['solution'].widget.attrs |= dir_attrs

    class Meta:
        model = ProblemSubmission
        fields = ['ltr_dir', 'solution', 'file']
        widgets = {
            'ltr_dir':
            forms.CheckboxInput(
                attrs={
                    'style': 'position:inherit;margin-left:4px;',
                    'onclick': "change_dir('MathInput')"
                }),
            'solution':
            forms.Textarea(attrs={'id': 'MathInput'})
        }
        labels = {
            'ltr_dir': 'الكتابة من اليسار',
            'solution': '',
            'file': 'إرفاق ملف'
        }

    def clean(self):
        if not self.cleaned_data['solution'] and not self.cleaned_data['file']:
            raise ValidationError(
                'يجب أن تقوم بكتابة إجابة، أو رفع ملف يحتوي على الإجابة.')
        return super().clean()


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['ltr_dir', 'content']
        widgets = {
            'content':
            forms.Textarea(attrs={
                'id': 'MathInput',
            }),
            'ltr_dir':
            forms.CheckboxInput(attrs={
                'style': 'position:inherit;margin-left:4px;',
                'onclick': "change_dir()",
            }, ),
        }
        labels = {'content': ''}
