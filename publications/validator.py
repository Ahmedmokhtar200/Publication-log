from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from publications.models import ProjectInfo, Email
from PIL import Image
from publications.models import Publication
import os

ext_validator = FileExtensionValidator(['jpg', 'jpeg', 'png'])



def validate_image(file):
    # Allowable extensions for images
    allowed_image_extensions = ['jpg', 'jpeg', 'png']

    # Extract the file extension
    ext = os.path.splitext(file.name)[1][1:].lower()  # Get file extension without the dot

    # Validate file extension
    if ext not in allowed_image_extensions:
        raise ValidationError("Unsupported image file type.")

    # Validate the image by trying to open and verify it
    try:
        img = Image.open(file)
        img.verify()  # Verify that it's a valid image file
    except (IOError, SyntaxError) as e:
        raise ValidationError("The uploaded file is not a valid image.")


def validate_file(file):
    # Allowed extensions for document files
    allowed_document_extensions = ['pdf', 'doc', 'docx']

    # Extract the file extension
    ext = os.path.splitext(file.name)[1][1:].lower()  # Get file extension without the dot

    # Validate file extension
    if ext not in allowed_document_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(allowed_document_extensions)}.")


def validate_unique_publication_title(value):
    if Publication.objects.filter(title=value).exists():
        raise ValidationError("This publication name already exists. Please choose a different name.")

