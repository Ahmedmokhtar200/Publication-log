from django.urls import path
from projects import views

app_name = 'projects'


urlpatterns = [
    path('', views.index, name="index"),
    # create
    path('create/', views.create, name='create'),
    # create collaborators
    path('<int:project_id>/collaborators/', views.create_collaborators, name='collaborator'),
    # edit
    path('edit/<int:project_info_id>/info', views.edit, name='edit'),
    # collaborators
    path('edit/<int:project_info_id>/collaborators', views.edit_collaborators, name='edit_collaborators'),
    # delete
    path('<int:project_info_id>/delete', views.delete, name='delete'),

    #
    # path('project/<int:project_id>/proposal/', views.create_proposal, name='proposal'),
    #
    # # path('create-project/', views.create_project, name='create_project'),
    #
    # path("check-email/", views.check_email, name='check-email'),
]
