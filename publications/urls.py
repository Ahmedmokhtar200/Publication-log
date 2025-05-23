from django.urls import path
from publications import views

app_name = 'publications'

urlpatterns = [
    path('', views.home, name='home'),
    #  http://localhost:8080/dashboard/
    path('dashboard/', views.dashboard, name='dashboard'),# maybe i create app for dashboard
    # show
    path('<int:publication_id>/show/', views.show, name='show'),

    path('<int:publication_id>/download/', views.download_publication_file, name='download_publication_file'),
    # create
    path('<int:project_info_id>/create', views.create, name='create'),
    # delete
    path('<int:project_info_id>/delete', views.delete, name='delete'),
    # create authors
    path('<int:publication_id>/authors/create', views.add_authors, name='authors'),

    path('<int:publication_id>/get/authors/', views.get_authors, name='get_authors'),

    path('<int:publication_id>/store/authors/', views.store_authors, name='store_authors'),

    path('get', views.search_publication, name='search_publication'),

    #
    # path('collaborators/<int:human_id>/<int:project_id>/', views.collaborator, name='collaborator'),
    #
    # path('collaborator/createform/<int:human_id>/<int:project_id>', views.collaborator_form, name='collaborator_form'),
    #
    # path('project/<int:project_id>/proposal/', views.create_proposal, name='proposal'),
    #
    # # path('create-project/', views.create_project, name='create_project'),
    #
    # path("check-email/", views.check_email, name='check-email'),
]







