from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from .serializers import *
from .models import *
from .serializers import *

class CreateHackathon(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        try:
            hackathon = Hackathon.objects.create(
                hosted_by=request.user,
                title = data['title'],
                background_image = data['bgimage_url'],
                hackathon_image = data['hcktimage_url'],
                submission_type = data['submission_type'],
                start_datetime = data['start_datetime'],
                end_datetime = data['end_datetime'],
                prize_amount = data['prize_amount']
            )
            seralized_data = HackathonSerializer(hackathon).data 
            return Response({'success':True, 'hackathon_data':seralized_data}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'success':False, 'message':'Please input all data'}, status=status.HTTP_400_BAD_REQUEST)

class ViewHackathons(APIView):
    def get(self,request):
        all_hackathons = Hackathon.objects.filter(end_datetime__gte=timezone.now())
        serialized_data = HackathonenrolledSerializer(all_hackathons,many=True).data
        return Response({'success':True,'hackathons':serialized_data}, status=status.HTTP_202_ACCEPTED)

class Enrol(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        try:
            hackathon_id = data['hackathon_id']
            hackathon_obj = Hackathon.objects.get(id = hackathon_id)
            if hackathon_obj.end_datetime<timezone.now():
                return Response({'success':False, 'message':'Hackathon expired'}, status=status.HTTP_400_BAD_REQUEST)
            enrl_obj = Enrolment.objects.filter(user = request.user,hackathon = hackathon_obj)
            if len(enrl_obj)>0:
                return Response({'success':False, 'message':'Already Enrolled'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                enrl_obj = Enrolment.objects.create(user = request.user,hackathon = hackathon_obj)
                serialized_data = EnrollmentSerializer(enrl_obj).data
                return Response({'success':True, 'hackathon_data':serialized_data}, status=status.HTTP_202_ACCEPTED)
        except Exception:
            return Response({'success':False, 'message':'Hackathon does not exist'}, status=status.HTTP_400_BAD_REQUEST)