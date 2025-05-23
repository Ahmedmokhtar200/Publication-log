from django.db import models
# from allauth.account.models import EmailAddress as AllauthEmailAddress
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class Human(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class HumanInfo(models.Model):
    first_name = models.CharField(max_length=255, default=None)
    last_name = models.CharField(max_length=255, default=None)
    city = models.CharField(max_length=255, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    human = models.ForeignKey(Human, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + '' + self.last_name


class Email(models.Model):
    address = models.CharField(max_length=255, unique=True)
    human_info = models.ForeignKey("HumanInfo", on_delete=models.CASCADE)

    def __str__(self):
        return f"Email address's {self.address}"


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class ProjectInfo(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    scientific_case = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Conference(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Collaborator(models.Model):
    project_info = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)


class Proposal(models.Model):
    project_info = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    duration = models.IntegerField()
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Publication(models.Model):
    title = models.CharField(max_length=255)
    project_info = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    image = models.FileField(upload_to='uploads/images/')
    file = models.FileField(upload_to='uploads/publications')# pdf file
    year = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    authors = models.ManyToManyField(Human, through="PublicationAuthor")

    def __str__(self):
        return self.title


class PublicationAuthor(models.Model):
    human_info = models.ForeignKey(Human, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)


class Action(models.Model):
    name = models.CharField(max_length=255)


class Event(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    source = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class EventProposal(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE)
    project_info = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)


class EventProject(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    project_info = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)



# class EmailAddress(AllauthEmailAddress):
#     class Meta:
#         verbose_name = _("email address")
#         verbose_name_plural = _("email addresses")
#         # Remove any constraints here if you want to avoid the MySQL warning
#         constraints = []  # or customize as needed