from django import forms

from projects.validators import validate_unique_project_title, validate_email_exists
from publications.models import *


class ProjectInfoForm(forms.ModelForm):
    title = forms.CharField(validators=[validate_unique_project_title])
    project_id = forms.IntegerField(required=False)

    class Meta:
        model = ProjectInfo
        fields = ['title', 'summary', 'scientific_case']  # Ensure you include the fields from the model

    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title

    def save(self, commit=True, project_id=None):
        # Get the unsaved instance from the form
        instance = super(ProjectInfoForm, self).save(commit=False)

        # Manually assign the project_id if passed
        if project_id:
            instance.project_id = project_id

        # Print instance data (fields) before saving
        print(f"Title: {instance.title}")
        print(f"Summary: {instance.summary}")
        print(f"Scientific Case: {instance.scientific_case}")
        print(f"Project ID: {instance.project_id}")

        if commit:
            instance.save()

        return instance