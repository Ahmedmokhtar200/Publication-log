from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from publications.models import Publication, ProjectInfo, Conference
from publications.forms import PublicationForm
import tempfile

# Create your tests here.


class CreatePublicationTest(TestCase):
    def setUp(self):
        # Create a ProjectInfo and Conference for the test
        self.project_info = ProjectInfo.objects.create(
            title='Test Project',
            summary='Test Summary',
            scientific_case='Test Scientific Case',
            project_id=1  # Make sure this ID exists in your Project model
        )

        self.conference = Conference.objects.create(
            name='Test Conference'
        )

    def test_create_publication_with_valid_data(self):
        # Prepare the file (optional)
        file = SimpleUploadedFile("test_file.pdf", b"file_content", content_type="application/pdf")

        # Prepare valid form data
        valid_data = {
            'title': 'Test Publication',
            'project_info': self.project_info.id,
            'conference': self.conference.id,
            'year': 2024,
            'url': 'https://drive.google.com/test-publication',
            # 'file' and 'image' are optional; let's just test one
        }

        response = self.client.post(reverse('publications:create'), valid_data)

        # Check if the response redirects (on success)
        self.assertEqual(response.status_code, 302)

        # Ensure that the publication was created in the database
        self.assertTrue(Publication.objects.filter(title='Test Publication').exists())

    def test_create_publication_without_required_fields(self):
        # Test missing required field 'url'
        invalid_data = {
            'title': 'Test Publication',
            'project_info': self.project_info.id,
            'conference': self.conference.id,
            'year': 2024,
            'url': '',  # URL is required, so we leave it empty
        }

        response = self.client.post(reverse('publications:create'), invalid_data)

        # Ensure the form does not validate and returns the form with errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'url', 'This field is required.')

    def test_create_publication_with_invalid_file(self):
        # Test with invalid file type for file field
        invalid_file = SimpleUploadedFile("test_file.txt", b"file_content", content_type="text/plain")

        invalid_data = {
            'title': 'Test Publication',
            'project_info': self.project_info.id,
            'conference': self.conference.id,
            'year': 2024,
            'url': 'https://drive.google.com/test-publication',
            'file': invalid_file  # Invalid file type (expecting pdf/doc/docx)
        }

        response = self.client.post(reverse('publications:create'), invalid_data)

        # Ensure that the form returns an error for the invalid file
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'file', 'Unsupported file type.')