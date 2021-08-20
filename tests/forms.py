from django import forms
from django.forms import widgets
from .models import TestAnswer

class UploadFileForm(forms.ModelForm):
    
    def save(self, **kwargs):
        setattr(self.instance, 'pb_pk', kwargs['pb_pk'])
        super().save(commit=True)
        self.instance.set_file_uploaded(kwargs['pb_num'])
        self.instance.set_files_path()
        self.instance.save(update_fields=['files', 'uploaded_files'])
    
    class Meta:
        model = TestAnswer
        fields = ['files']
    