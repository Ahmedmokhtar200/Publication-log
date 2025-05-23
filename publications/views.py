import json

from django.db.models import Prefetch, OuterRef, Exists
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
# from allauth.account.models import EmailAddress
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import CustomSignupForm, CollaboratorForm, ProjectInfoForm, ProposalForm, PublicationForm
from publications.models import HumanInfo, ProjectInfo, Email, Human, Collaborator, Project, Proposal, Publication, \
    PublicationAuthor, Action, Event, EventProject
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User, AbstractUser
from django.contrib import messages
from allauth.account.views import SignupView, LoginView, LogoutView
from django.db.models import Min, Max
from django.utils import timezone
from django.forms import inlineformset_factory
from django.core.exceptions import ObjectDoesNotExist
import re as r
import random
import collections


class ProjectList(ListView):
    model = ProjectInfo

    def get_queryset(self):
        return ProjectInfo.objects.all()


class CustomSignupView(SignupView):
    form_class = CustomSignupForm
    template_name = 'account/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form is None:
            print("form is none")
        # print(form)
        print(f"Response type: {type(request)}")

        print("after initializing form")
        if form.is_valid():
            print("after form is valid")

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            city = form.cleaned_data['city']
            password1 = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            username = email

            human_info = HumanInfo.objects.create(first_name=first_name, last_name=last_name, city=city)
            print("after user is created")
            # I changed email to connected to human_id because email cannot change
            # or else how can I connect user to human
            Email.objects.create(human_info_id=human_info.id, address=email)
            print("after email is created")
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email,
                                     password=password1)
            print("after user is created")

            return redirect('account_login')
        else:
            # If form is invalid, print the errors and re-render the form
            print(form.errors)
            return self.form_invalid(form)


class CustomLoginView(LoginView):

    def form_valid(self, form):
        # get human_id and email
        email = form.cleaned_data.get('login')

        e = Email.objects.get(address=email)

        human_id = e.human_info.human_id

        # Store the project_info_ids in the session
        collaborations = Collaborator.objects.filter(email=e)

        project_infos_ids = list(collaborations.values_list('project_info_id', flat=True))
        print(project_infos_ids)
        # how
        projects = Project.objects.filter(projectinfo__in=project_infos_ids)
        print(projects)

        self.request.session['email'] = email
        self.request.session['human_id'] = human_id
        session = self.request.session['projects'] = list(projects.values_list('id', flat=True))

        print(f"session is {session}")
        # # After successful form validation and login
        user = form.user  # Get the authenticated user

        # Assuming 'has_header' is a method of your user model
        if user:
            print("User logged in successfully")
            return super().form_valid(form)  # Let Allauth handle the login process
        else:
            # User is authenticated but doesn't have the required 'has_header' attribute
            return HttpResponse(status=400)

    def get_success_url(self):
        # Redirect to 'publications/home' after successful login
        return reverse('publications:home')


class CustomLogoutView(LogoutView):

    def get_redirect_url(self):
        # Redirect to 'publications/home' after successful login
        return reverse('publications:home')


def custom_redirect_view(request):
    return redirect('publications:home')


class CreateCollaborator(FormView):
    form_class = CollaboratorForm
    template_name = 'publications/partials/collaborator_form.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            email_form = form.cleaned_data['email']
            project_form = form.cleaned_data['project_info']
            email = Email.objects.get(address=email_form)
            project_title = ProjectInfo.objects.get(name=project_form)
            Collaborator.objects.create(project_title=project_title, email_id=email, )
            # collaborator = form.save()

            return redirect('proposal')

        return HttpResponse('not working')


def create_proposal(request, project_id):
    project_info = get_object_or_404(ProjectInfo, pk=project_id)
    if request.method == "POST":
        form = ProposalForm(request.POST)
        if form.is_valid():
            duration = form.cleaned_data['duration']
            Proposal.objects.create(duration=duration, project_info=project_info)
            return redirect('dashboard')
    form = ProposalForm
    context = {'form': form, 'project': project_info}
    return render(request, 'publications/proposal_page.html', context)


def get_proposal(request):
    return render(request, 'publications/proposal_page.html', {})


def is_post(request):
    return request.method == 'POST'


def suggest_email(request):
    address = request.GET.get('email')
    payload = []
    if address:
        emails = Email.objects.filter(address__icontains=address)
        for email in emails:
            payload.append(email.address)

    return JsonResponse({'status': 200, 'data': payload})


def home(request):
    publications = Publication.objects.all()
    return render(request, 'publications/home.html', {'publications': publications})


# step 1 dashboard has project_id when i press publication i create project
# for specific project
#
# dashboard has all projects , all publication associated within project
def create(request, project_info_id):
    project_info = ProjectInfo.objects.get(pk=project_info_id)
    print(project_info)
    if request.method == "POST":

        form = PublicationForm(request.POST, request.FILES)
        print(request.FILES)

        if form.is_valid():
            publication = form.save()
            image_action = None
            file_action = None
            try:
                if request.FILES.get("image"):
                    image_action = Action.objects.get(name="image_file")
                if request.FILES.get("file"):
                    file_action = Action.objects.get(name="upload_file")
            except (Action.DoesNotExist, Action.MultipleObjectsReturned):
                if request.FILES.get("image"):
                    image_action = Action.objects.create(name="upload_image")
                if request.FILES.get("file"):
                    file_action = Action.objects.create(name="upload_file")

            try:
                action = Action.objects.get(name="create_publication")
            except (Action.DoesNotExist, Action.MultipleObjectsReturned):
                action = Action.objects.create(name="create_publication")

            # publication event
            event_project = Event.objects.get(action__name="create_project",
                                              eventproject__project_info=project_info)
            event = Event.objects.create(action=action, source_id=event_project.id, success=1)

            EventProject.objects.create(project_info=project_info, event=event)

            # image and file event
            #
            if image_action:
                Event.objects.create(action=image_action, source_id=event.id)
                EventProject.objects.create(project_info=project_info, event=event)
            if file_action:
                Event.objects.create(action=file_action, source_id=event.id)
                EventProject.objects.create(project_info=project_info, event=event)

            return redirect('publications:authors', publication.id)
        else:
            print(form.errors.as_data())
            print(form.errors.get('title'))
            context = {'form': form, 'project_info': project_info}
            return render(request, 'publications/publication_form.html', context)

    form = PublicationForm()
    context = {'form': form, 'project_info': project_info}
    return render(request, 'publications/publication_form.html', context)


def show(request, publication_id):
    publication = Publication.objects.get(pk=publication_id)
    project_info = ProjectInfo.objects.get(publication=publication)
    # Assuming the PublicationAuthor model has a field called `email`
    authors = PublicationAuthor.objects.filter(publication=publication)
    # Retrieve all the email addresses associated with the publication
    first_names = HumanInfo.objects.filter(id__in=authors.values('human_info_id'))
    emails = Email.objects.filter(human_info__in=authors.values('human_info_id'))
    context = {
        'publication': publication,
        'authors': first_names,
        'emails': emails,
        'project_info': project_info,
    }

    return render(request, 'publications/publication_show.html', context)


def download_publication_file(request, publication_id):
    try:
        publication = Publication.objects.get(pk=publication_id)
        file_path = publication.file.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # Assuming a PDF file
    except Publication.DoesNotExist:
        raise Http404("Publication does not exist")


# in dashboard context contain updated project_info and publication id
def dashboard(request):
    user = request.user
    if user.is_authenticated:
        print(user.first_name)

        # OuterRef('pk'): This references the Project's primary key in the outer query.

        # project_ids = request.session.get('projects', [])
        projects = get_projects(user.email)
        # projects = Project.objects.filter(id__in=project_ids)

        # print(f"exculed project{event_subquery}")
        print(f"project{projects}")

        project_publication = get_publications_associated_with_project(projects)

    else:
        email = ""
        human_info = ""
        projects = ""
        project_publication = ""

    context = {
        'user': user,
        # 'human_id': human_info,
        'project_publication': project_publication,

    }
    return render(request, 'dashboard.html', context)


def get_publications_associated_with_project(projects):
    # Get the minimum 'id' (which is the first publication from the bottom) for each project
    project_infos = ProjectInfo.objects.filter(project_id__in=projects) \
        .values('project_id') \
        .annotate(max_id=Max('id')) \
        .values_list('max_id', flat=True)

    print(f"project info of {project_infos}")

    # Initialize a list to hold tuples of project_info and its publications
    project_with_publications = []

    # all events that has delete_publication in project_info_ids
    # print publications now***
    # deleted_publications = None
    # project_deleted_publications = None
    event_project = Event.objects.filter(eventproject__project_info__in=project_infos,
                                         action__name="delete_publication",
                                         deleted_at__isnull=False).values_list('id', flat=True)
    print(event_project)
    # project_infos_ids = project_infos.values_list("project_id", flat=True)
    # print(f"project_infos_ids {project_infos_ids}")
    # x = ProjectInfo.objects.filter(eventproject__in=event_project)
    # print(f"x is{x}")
    print(f"event project {list(event_project)}")

    # deleted_publications = Publication.objects.filter(project_info_id__in=x)
    deleted_publications = Publication.objects.filter(project_info__eventproject__in=event_project)
    print(deleted_publications)
    print(f"deleted_publications i want {deleted_publications}")
    # Loop through each project_info
    for project_info in ProjectInfo.objects.filter(id__in=project_infos):

        # Get the publications associated with this project_info
        related_publications = Publication.objects.filter(project_info_id=project_info.id)

        if deleted_publications:
            # # Get the deleted publications specific to this project_info
            project_deleted_publications = deleted_publications.filter(project_info_id=project_info.id)
            print(project_deleted_publications)

            # Compare related and deleted publications for this specific project_info
            if list(related_publications) == list(project_deleted_publications):
                project_with_publications.append((project_info, None))
                continue
        # Append a tuple of project_info and its related publications to the list
        project_with_publications.append((project_info, related_publications))

    print(f"i dont want climate change and coastal biodiversity")
    print(project_with_publications)
    return project_with_publications


def get_projects(email):
    # # get human_id and email
    # email = form.cleaned_data.get('login')

    e = Email.objects.get(address=email)

    human_id = e.human_info.human_id

    # Store the project_info_ids in the session
    collaborations = Collaborator.objects.filter(email=e)
    project_infos_ids = list(collaborations.values_list('project_info_id', flat=True))
    print(project_infos_ids)

    event_project = EventProject.objects.filter(project_info__in=project_infos_ids,
                                                event__action__name="delete_project",
                                                event__deleted_at__isnull=False)

    print(event_project.values_list('project_info', flat=True))
    # Remove all event_project_ids from project_infos_ids
    project_infos_ids = [project_info_id for project_info_id in project_infos_ids
                         if project_info_id not in list(event_project.values_list('project_info', flat=True))]
    print(project_infos_ids)
    # event_subquery = EventProject.objects.filter(project_info_id=OuterRef('pk'), deleted_at__isnull=False)
    # project_infos_ids = list(collaborations.values_list('project_info_id', flat=True))

    # print(project_infos_ids)
    projects = Project.objects.filter(projectinfo__in=project_infos_ids)
    print(projects)

    return projects


def add_authors(request, publication_id):
    return render(request, 'publications/authors.html', {'publication_id': publication_id})


def get_authors(request, publication_id):
    # all emails within collaborator
    # from publication_id get project_info_id
    # from project_id get all collaborators within that project_info_id
    #
    project_info = ProjectInfo.objects.filter(publication__id=publication_id)  # 403
    collaborators = Collaborator.objects.filter(project_info__in=project_info)
    emails = Email.objects.filter(id__in=collaborators.values('email_id'))

    # advanced way to get emails
    # emails = Email.objects.filter(
    #     collaborator__project_info__publication__id=102
    # )

    authors = []
    for email in emails:
        human_info = HumanInfo.objects.get(email=email)
        author_info = [
            human_info.first_name,
            email.address,

        ]
        authors.append(author_info)
    # data = list(email)
    return JsonResponse(authors, safe=False)


@csrf_exempt
def store_authors(request, publication_id):

    # Parse the JSON data from the POST request
    data = json.loads(request.body)
    print(data)

    # Check if the data (authors list) is empty
    if not data.get('authors'):
        # Redirect to the same page (no authors submitted)
        return JsonResponse({'redirect': reverse('publications:get_authors', args=[publication_id])})

    # Extract the list of authors 7ass feh 7aga 8alat f human_info
    authors = data.get('authors', [])
    print(authors)
    for author in authors:
        email = Email.objects.get(address=author['email'])
        human_info = HumanInfo.objects.get(email=email)
        PublicationAuthor.objects.create(
            publication_id=publication_id,
            human_info_id=human_info.id
        )
        # redirect
        # response = HttpResponse(status=301)
        # response["HX-Redirect"] = reverse_lazy("publications:dashboard")
    redirect_url = reverse('publications:dashboard')  # Get the URL for the target view

    return JsonResponse({'redirect': redirect_url})  # Return the redirect URL in a JSON response


def delete(request, project_info_id):
    project_info = get_object_or_404(ProjectInfo, pk=project_info_id)
    # project = Project.objects.get(pk=project_info.project_id)
    try:
        action = Action.objects.get(name="delete_publication")
    except Action.DoesNotExist:
        action = Action.objects.create(name="delete_publication")

    previous_action = Event.objects.filter(action__name="create_publication",
                                           eventproject__project_info=project_info).first()
    # source should be changed
    # source id 10
    # source_id action create project_info_id equal project_info_id
    event = Event.objects.create(action=action, source_id=previous_action.id, success=1, deleted_at=timezone.now())
    event_project = EventProject.objects.create(event=event, project_info_id=project_info_id)
    print(event)

    return redirect('publications:dashboard')


def search_publication(request):
    return None
