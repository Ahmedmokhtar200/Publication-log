from django.core.exceptions import ValidationError
from publications.models import ProjectInfo, Email


def validate_unique_project_title(value):
    if ProjectInfo.objects.filter(title=value).exists():
        raise ValidationError("This project name already exists. Please choose a different name.")


def validate_email_exists(value):
    email_address = value

    if not Email.objects.filter(address=email_address).exists():
        raise ValidationError("This Email does not exist")

