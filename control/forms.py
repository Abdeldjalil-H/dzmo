from django import forms

from accounts.models import User
from lessons.models import Chapter

LEVELS = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]


class AddProblemsForm(forms.Form):
    statements = forms.CharField(widget=forms.Textarea(), label="المسائل")
    chapter = forms.ModelChoiceField(queryset=Chapter.objects.all(), label="المحور")
    level = forms.ChoiceField(choices=LEVELS, label="المستوى")


class SendMailForm(forms.Form):
    subject = forms.CharField(label="الموضوع")
    msg = forms.CharField(widget=forms.Textarea(), label="الرسالة")
    receivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="المستقبلون",
    )
    to_all_students = forms.BooleanField(required=False, label="    جميع التلاميذ    ")
    to_all_staff = forms.BooleanField(required=False, label="   جميع المشرفين    ")
