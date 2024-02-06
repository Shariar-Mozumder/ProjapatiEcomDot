from django.urls import path,include
from . import views

urlpatterns = [
    # User APIs
    path('getAllUsers/', views.getAllUser),
    path('registration/', views.registration),
    path('login/', views.login)
]