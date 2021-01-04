from django.db.models.signals import post_save
from problems.models import ProblemSubmission
from .models import CorrectorsNotif
def send_notif_to_correcters(sender, instance, created, **kwargs):
    notif_settings = CorrectorsNotif.objects.first()
    if notif_settings:
        if instance.status in ['submit', 'comment']:
            notif_settings.have_to_send_mail()
        elif instance.status in ['correct','wrong']:
            notif_settings.add_corrected_problem()


post_save.connect(send_notif_to_correcters, sender = ProblemSubmission, weak = False)