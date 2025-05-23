from django.urls import path, include
from accounts import views

urlpatterns = [
    path('login/', views.CustomLogInView.as_view(), name='login'),
    path('signup/', views.CustomSignupView.as_view(), name='signup'),
]
