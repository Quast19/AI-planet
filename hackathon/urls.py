from django.urls import path
from .views import *

urlpatterns = [
    path('create',CreateHackathon.as_view()),
    path('view',ViewHackathons.as_view()),
    path('enrol',Enrol.as_view()),
]
