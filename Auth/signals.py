from django.db.models.signals import post_save
from .models import Account, Club, Member
from django.dispatch import receiver
from SecReport.models import DuesPaid

@receiver(post_save, sender=Account)
def createProfile(sender, instance, created, **kwargs) :
    if created and instance.loginType=='1':
        club = Club.objects.create(clubName=instance.username, login=instance)
        club.save()
        DuesPaid.objects.create(club = club)

        
