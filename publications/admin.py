from django.contrib import admin

# from .forms import CollaboratorRequestsForm
from .models import *
# Register your models here.


class InlineEventProposal(admin.StackedInline):
    model = EventProposal
    extra = 1


class InlineCollaborator(admin.StackedInline):
    model = Collaborator
    extra = 1

class InlineAction(admin.StackedInline):
    model = Action
    extra = 1


class InlinePublication(admin.StackedInline):
    model = Publication
    extra = 1


class InlineProject(admin.StackedInline):
    model = Project
    extra = 1


class InlineProposal(admin.StackedInline):
    model = Proposal
    extra = 1


class InlineEvent(admin.StackedInline):
    model = Event
    extra = 1


class InlinePublicationAuthor(admin.StackedInline):
    model = PublicationAuthor
    extra = 1


class CustomHuman(admin.ModelAdmin):
    fieldsets = [
        ('Human', {
            'fields': [
                'first_name',
                'last_name',
                'city'
            ],
        }),

    ]
    list_display = ['first_name', 'last_name', 'city']
    list_filter = ['city']
    search_fields = ['first_name']


class CustomPublication(admin.ModelAdmin):
    fieldsets = [
        ('Publication Information', {
            'fields': [
                'title',
                'url',
                'year',
                'project',
                'conference',

            ],
        }),
    ]
    inlines = [InlinePublicationAuthor]


# class CustomProject(admin.ModelAdmin):
#     fieldsets = [
#         ('Project Information', {
#             'fields': [
#                 'title',
#                 'summary',
#                 'scientific_case',
#             ],
#         }),
#     ]
#     inlines = [InlinePublication, InlineProposal]
#     list_display = ['title', 'scientific_case', 'verified']
#     list_filter = ['scientific_case']
#     search_fields = ['scientific_case']


class CustomProposal(admin.ModelAdmin):
    fieldsets = [
        ('Proposal Information', {
            'fields': [
                'project',
                'duration',
                'submitted',
            ],
        }),
    ]
    inlines = [InlineEventProposal]
    search_fields = ['project_title']


class CustomCollaborator(admin.ModelAdmin):
    fieldsets = [
        ('Collaborator Information', {
            'fields': [
                'project',
                'email'
            ],
        }),
    ]


class CustomEvent(admin.ModelAdmin):
    fieldsets = [
        ('Event Information', {
            'fields': [
                'success',
                'action'
            ],
        }),
    ]
    inlines = [InlineEventProposal]


class EventProposal(admin.ModelAdmin):
    fieldsets = [
        ('Proposal Information', {
            'fields': [
                'event',
                'proposal'
            ],
        }),
    ]


class CustomAction(admin.ModelAdmin):
    fieldsets = [
        ('Action Information', {
            'fields': [
                'name'
            ],
        }),
    ]


class CustomEmail(admin.ModelAdmin):
    fieldsets = [
        ('Email Information', {
            'fields': [
                'address',
            ],
        }),
    ]


class CustomConference(admin.ModelAdmin):
    fieldsets = [
        ('Conference Information', {
            'fields': [
                'name',
            ],
        }),
    ]
    inlines = [InlinePublication]


# class ProjectRequests(admin.ModelAdmin):
#     form = ProjectInfo
#     fieldsets = [
#         (None, {
#             'fields': [
#                 '',
#             ],
#         }),
#     ]



admin.site.register(HumanInfo, CustomHuman)
admin.site.register(Publication, CustomPublication)
# admin.site.register(ProjectInfo, CustomProject)
admin.site.register(Proposal, CustomProposal)
admin.site.register(Collaborator, CustomCollaborator)
admin.site.register(Event, CustomEvent)
admin.site.register(Action, CustomAction)
admin.site.register(Email, CustomEmail)
admin.site.register(Conference, CustomConference)
# admin.register(ProjectRequests)
