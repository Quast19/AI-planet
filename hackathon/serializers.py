from .models import *
from rest_framework import serializers
from accounts.serializers import DisplaySerializer

class HackathonSerializer(serializers.ModelSerializer):
    hosted_by = DisplaySerializer()
    class Meta:
        model = Hackathon
        fields = ('id','title','hosted_by','background_image','hackathon_image','submission_type','start_datetime','end_datetime','prize_amount')
    
class HackathonenrolledSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ('id','title','hackathon_image','start_datetime','end_datetime','prize_amount','submission_type')

class EnrollmentSerializer(serializers.ModelSerializer):
    hackathon = HackathonenrolledSerializer()
    user = DisplaySerializer()
    class Meta:
        model = Enrolment
        fields = ('user','hackathon','enrollment_date')

