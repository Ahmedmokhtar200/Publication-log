import sys

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ProjectInfoForm
from publications.models import Project, ProjectInfo, Collaborator, Email, HumanInfo, Publication, EventProject, Action, Event
from .validators import validate_email_exists
from django.utils import timezone

# Create your views here.


def home(request):
    return HttpResponse("i am here in projects")


def index(request):
    form = ProjectInfoForm
    context = {'form': form}
    return render(request, 'projects/project_page.html', context)


def create(request):
    print(request.method)

    if request.method == "POST":
        form = ProjectInfoForm(request.POST)
        # project == projectinfo
        if form.is_valid():
            project = form.save()  # This saves the model instance automatically
            print(project)
            project_id = project.project_id
            # Retrieve the existing 'projects' from session or initialize it as an empty list
            projects = request.session.get('projects', [])

            # Append the new project_id to the existing list
            projects.append(project_id)

            # Save the updated list back into the session
            request.session['projects'] = projects
            print(f"Updated session with project IDs: {projects}")
            try:
                action = Action.objects.get(name="create_project")
            except (Action.DoesNotExist, Action.MultipleObjectsReturned):
                action = Action.objects.create(name="create_project")

            event = Event.objects.create(action=action, source_id=None, success=1)

            event_project = EventProject.objects.create(project_info=project, event=event)

            return redirect('projects:collaborator', project_id)
        else:
            print(form.errors.get("title"))
            print(form.errors.as_data())
            context = {"form": form}
            return render(request, "projects/project_page.html", context)
    # get request
    form = ProjectInfoForm()
    context = {'form': form}
    return render(request, 'projects/project_page.html', context)


def create_collaborators(request, project_id):
    create_url = 'http://127.0.0.1:8000/projects/create/'
    collaborators_url = f'http://127.0.0.1:8000/projects/{project_id}/collaborators/'

    if not is_allowed(create_url, request) or not is_allowed(collaborators_url, request):
        return HttpResponseForbidden("Access Denied: Invalid Referrer")

    if request.method == "POST":
        # Collect all email fields from the request POST data
        emails = [value for key, value in request.POST.items() if key.startswith('email')]

        all_valid = True
        invalid_emails = []
        duplicate_emails = []

        # Check for duplicate emails first
        seen_emails = set()
        for email in emails:
            if email in seen_emails:
                duplicate_emails.append(email)
            else:
                seen_emails.add(email)

        # If there are duplicate emails
        if duplicate_emails:
            all_valid = False
            error_message = "Cannot enter duplicate emails: " + ', '.join(duplicate_emails)
            return render(request, 'projects/collaborator_page.html', {
                'project_id': project_id,
                'emails': emails,  # Pass back the emails to show them in the form
                'error_message': error_message
            })
        # Loop through the emails and validate each one
        for email in emails:
            try:
                # Use your custom validator to check if the email exists
                validate_email_exists(email)
            except ValidationError:
                all_valid = False
                invalid_emails.append(email)

        # If all emails are valid
        if all_valid:
            # get updated project
            project_info = ProjectInfo.objects.filter(project_id=project_id).last()
            # create project collaborator foreach email
            for email in emails:
                email = Email.objects.get(address=email).id
                print(project_info)
                collaborator = Collaborator.objects.create(email_id=email, project_info=project_info)

            # insert user as collaborator in project
            # get last row which has human_id of user
            human = request.session.get('human_id')
            print(f"human id is {human}")
            human_info = HumanInfo.objects.filter(human_id=human).last()
            print(f"human_info id is {human_info} + human_info_id is {human_info.human_id}")
            email = Email.objects.get(human_info_id=human_info.id)
            print(f"email id is {email}")
            Collaborator.objects.create(email_id=email.id, project_info_id=project_info.id)

            # store project_ids in session to make dashboard url looks clean
            if 'project_ids' not in request.session:
                request.session['project_ids'] = []

            # Append the new project_id to the session list (if it's not already there)
            if project_id not in request.session['project_ids']:
                request.session['project_ids'].append(project_id)
            # Save the session explicitly to ensure changes are persisted
            request.session.modified = True
            return redirect('publications:dashboard')

        # If there are invalid emails
        else:
            error_message = "The following emails are invalid: " + ', '.join(invalid_emails)
            return render(request, 'projects/collaborator_page.html', {
                'project_id': project_id,
                'emails': emails,  # Pass back the emails to show them in the form
                'error_message': error_message
            })

    return render(request, "projects/collaborator_page.html", {'project_id': project_id})


def is_allowed(allowed_url, request):
    # Check if HTTP_REFERER is present and matches the allowed referer
    referer = request.META.get('HTTP_REFERER')
    # Check if the referer matches the allowed URL
    if referer and referer.startswith(allowed_url):
        return True
    else:
        return True


# edt project
def edit(request, project_info_id):
    project_info = get_object_or_404(ProjectInfo, pk=project_info_id)

    if request.method == "POST":
        # new_project_info = ProjectInfo.objects.create()
        form = ProjectInfoForm(request.POST, instance=ProjectInfo(
            project_id=project_info.project_id)) # this code because signal auto generate new project
        # to edit form -> ProjectInfoForm(request.POST, instance=project_info)

        if form.is_valid():
            # insert new project_info in publication
            new_project_info = form.save()
            # Get all publications associated with the old project_info_id
            old_publications = Publication.objects.filter(project_info_id=project_info_id)

            # Iterate through the old publications and create new ones with the new project_info_id
            for old_publication in old_publications:
                Publication.objects.create(
                    project_info=new_project_info,
                    title=old_publication.title,
                    conference=old_publication.conference,
                    year=old_publication.year,
                    image=old_publication.image,  # Copy image reference (file field)
                    url=old_publication.url,
                    file=old_publication.file  # Copy file reference (file field)
                )
            old_publications.delete()
            old_collaborators = Collaborator.objects.filter(project_info_id=project_info_id)
            for old_collaborator in old_collaborators:
                Collaborator.objects.create(
                    project_info=new_project_info,
                    email=old_collaborator.email,
                )

            return redirect('publications:dashboard')
        else:
            print(form.errors.as_data)
            context = {'form': form, 'project_info': project_info}
            return render(request, 'projects/project_edit.html', context)

    form = ProjectInfoForm(instance=project_info)
    context = {'form': form, 'project_info': project_info}
    return render(request, 'projects/project_edit.html', context)


def edit_collaborators(request, project_info_id):
    # get/send old collaborators
    # add/remove collaborators
    # get old collaborators
    # only insert new collaborators

    old_collaborators = Collaborator.objects.filter(project_info_id=project_info_id)
    context = {'collaborators': list(old_collaborators), 'project_info_id': project_info_id}
    return render(request, "projects/edit_collaborators.html", context)


def delete(request, project_info_id):
    project_info = get_object_or_404(ProjectInfo, pk=project_info_id)
    # project = Project.objects.get(pk=project_info.project_id)
    action = Action.objects.create(name="delete_project")

    # source should be changed
    event = Event.objects.create(action=action, source_id=None, success=1, deleted_at=timezone.now())
    event_project = EventProject.objects.create(event=event, project_info_id=project_info_id)

    return redirect('publications:dashboard')
