from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    print('Начало сигнала')
    print(f"{sender=}\n{instance=}\n{created=}\n{kwargs}")
    print('Конец сигнала')
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)