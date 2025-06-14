"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from publications import views
from publications.views import CustomSignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    # maybe make app accounts phase 2
    path("accounts/signup/", views.CustomSignupView.as_view(), name='account_signup'),
    path("accounts/login/", views.CustomLoginView.as_view(), name='account_login'),
    path("accounts/profile/", views.custom_redirect_view, name='google_login'),
    # path("accounts/profile/", views.dashboard, name='dashboard'),
    path("accounts/", include('allauth.urls')),
    path("publications/", include('publications.urls'), name="publications"),
    path("projects/", include('projects.urls'), name="projects"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


