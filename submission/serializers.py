from .models import *
from rest_framework import serializers
from accounts.serializers import DisplaySerializer
from hackathon.serializers import HackathonenrolledSerializer

class SubmissionSerializer(serializers.ModelSerializer):
    hackathon = HackathonenrolledSerializer()
    owner = DisplaySerializer()
    class Meta:
        model = Submission
        fields = ('id','hackathon','owner','created_at','type','updated_at','text_file','link','image_file')