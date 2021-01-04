from django.db.models.signals import post_save
from problems.models import ProblemSubmission
from .models import CorrectorsNotif
def send_notif_to_correcters(sender, instance, created, **kwargs):
    print(instance)
    if instance.status == 'submit':
        print('am here')
        notif_settings = CorrectorsNotif.objects.first()
        if notif_settings:
            notif_settings.have_to_send_mail()

post_save.connect(send_notif_to_correcters, sender = ProblemSubmission, weak = False)