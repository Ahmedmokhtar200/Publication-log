from django import forms
from publications.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm, LoginForm
from allauth.account.forms import SignupForm
from allauth.account.forms import BaseSignupForm
from django.forms import inlineformset_factory, formset_factory
from django.utils.timezone import now
from publications.validator import validate_image, validate_file, validate_unique_publication_title


class HumanForm(forms.ModelForm):
    class Meta:
        model = HumanInfo
        fields = ('first_name', 'last_name', 'city')


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = ('name',)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectInfo
        fields = ('title', 'summary', 'scientific_case',)

############# add verfication of project_info  /////////////////////
# class CollaboratorRequestsForm(forms.ModelForm):
#     verified = forms.BooleanField()
#
#     def save(self, commit=True):
#         verified = self.cleaned_data.get('verified', None)
#         # ...do something with extra_field here...
#         return super(ProjectForm, self).save(commit=commit)
#     class Meta:
#         model = ProjectInfo

# views forms ########
class CollaboratorForm(forms.Form):
    # increment = 1

    email = forms.CharField(
        label='Email',
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'id': 'email',

            }
        )
    )
    counter = forms.IntegerField()


# dont forget image
class PublicationForm(forms.ModelForm):

    class Meta:
        model = Publication
        fields = ('title', 'project_info', 'conference', 'year', 'url', 'file', 'image')
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'Enter link to your publication'}),
        }

    # url = forms.URLField(validators=[validate_url])
    # Mark image and file as optional in the form
    title = forms.CharField(validators=[validate_unique_publication_title])
    image = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': '.png,.jpg,.jpeg'}),
        validators=[validate_image])
    file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': '.docx,.doc,.pdf'}),
        validators=[validate_file])

    # because image, file uses validators
    def clean_title(self):
        title = self.cleaned_data.get('title')
        return title

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            # Get the file extension
            ext = image.name.split('.')[-1]

            # Create a new filename
            new_filename = f"{self.cleaned_data['title']}_{now().strftime('%Y%m%d%H%M%S')}.{ext}"

            # Rename the file
            image.name = new_filename

        return image

    def clean_file(self):
        file = self.cleaned_data.get('file')
        return file


        # # Ensure URL is always required
        # if not url:
        #     raise forms.ValidationError("You must provide a URL for the publication.")

        # At least one of file or image must be provided (but not mandatory if both are empty)
        # if not image and not file:
        #     raise forms.ValidationError("You must upload either an image or a file.")


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        label="First Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "First Name", }
        )
    )
    last_name = forms.CharField(
        label="Last Name",
        max_length=30,
        widget=forms.TextInput(
            attrs={"placeholder": "Last Name"}
        )
    )
    city = forms.CharField(
        label="City",
        max_length=50,
        widget=forms.TextInput(
            attrs={"placeholder": "City"}
        )
    )

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)


# class UploadProjectForm(forms.Form):
#
#     def __init__(self, *args, **kwargs):
#         super(UploadProjectForm, self).__init__(*args, **kwargs)
#         self.fields.update(ProjectForm().fields)
#         self.fields.update(CollaboratorFormSet().files)
#         self.fields.update(ProposalForm().fields)
#         # self.collaborator_formset = CollaboratorFormSet(*args, **kwargs)
#

class ProjectInfoForm(forms.Form):
    title = forms.CharField(
        label="Title",
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Title", }
        )
    )
    summary = forms.CharField(
        label="Summary",
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Summary", }
        )
    )
    scientific_case = forms.CharField(
        label="Scientific Case",
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Scientific Case", }
        )
    )

    def save(self):
        pass


class ProposalForm(forms.Form):
    duration = forms.CharField(
        label="Duration",
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Enter date", }
        )
    )



