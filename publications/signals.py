from django.dispatch import receiver
from django.db.models.signals import (post_save, pre_save)
from publications.models import (Human, HumanInfo, Project, ProjectInfo)
from django.contrib.auth.models import User


@receiver(pre_save, sender=HumanInfo)
def pre_save_human(sender, instance, *args, **kwargs):
    if not instance.pk:
        instance.human = Human.objects.create()


@receiver(pre_save, sender=ProjectInfo)
def pre_save_project(sender, instance, *args, **kwargs):
    if not instance.pk and not instance.project_id:
        instance.project = Project.objects.create()
        print(f"New Project created with ID: {instance.project_id}")
    else:
        print(f"Using existing Project with ID: {instance.project_id}")

# @receiver(post_save, sender=HumanInfo)
# def post_save_user(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.user = User.objects.create(instance.first_name, instance.last_name, instance.email)

#fk in humaninfo
#user --> humaninfo