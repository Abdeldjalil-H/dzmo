from django import forms
from .models import TestAnswer

class UploadFileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pb_pk = kwargs.get('pb_pk')
    
    def save(self, commit):
        setattr(self.instance, 'pb_pk', self.pb_pk)
        super().save(commit=commit)
        self.instance.set_files_path()
        self.instance.save()
    class Meta:
        model = TestAnswer
        fields = ['files']
    