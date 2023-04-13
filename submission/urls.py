from django.urls import path
from .views import *

urlpatterns = [
    path('create',CreateSubmission.as_view()),
]