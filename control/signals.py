from django.db.models.signals import post_save

from problems.models import ProblemSubmission

from .models import CorrectorsNotif


def send_notif_to_correcters(sender, instance, created, **kwargs):
    CorrectorsNotif.objects.first().update(instance.status)


post_save.connect(send_notif_to_correcters, sender=ProblemSubmission, weak=True)
