from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

#Dùng để default group là member khi đăng ký(để phân quyền)
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Member'))