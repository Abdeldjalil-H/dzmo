from django.db.models.signals import post_save
from .models import StudentProgress, User
def create_progress(sender, instance, created, **kwargs):
    if created:
        StudentProgress.objects.create(student = instance)
        print('porfile created')
post_save.connect(create_progress, sender = User, weak = False)
