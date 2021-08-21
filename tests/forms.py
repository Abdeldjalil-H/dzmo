from django import forms
from django.core.exceptions import ValidationError
from .models import TestAnswer

class UploadFileForm(forms.ModelForm):
    
    def save(self, **kwargs):
        setattr(self.instance, 'pb_num', kwargs['pb_num'])
        super().save(commit=True)
        self.instance.set_file_uploaded(kwargs['pb_num'])
        self.instance.set_files_path()
        self.instance.save()
    
    def clean(self):
        if not self.cleaned_data['files']:
            raise ValidationError('الرجاء إرفاق ملف')
        return super().clean()
    class Meta:
        model = TestAnswer
        fields = ['files']
    
class CorrectionForm(forms.Form):
    mark = forms.ChoiceField(choices=[(x,x) for x in range(8)])