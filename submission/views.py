from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from .serializers import *
from hackathon.models import Hackathon
from .serializers import *

class CreateSubmission(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        data = request.data
        try:
            hackathon_obj = Hackathon.objects.get(id=data['hackathon_id'],end_datetime__gte=timezone.now())
            enrl_obj = Enrolment.objects.filter(user=request.user,hackathon=hackathon_obj)
            if Submission.objects.filter(hackathon=hackathon_obj, owner=request.user).exists():
                return Response({'success':False,'message':'Submission already done, please edit the previous submission'}, status=status.HTTP_400_BAD_REQUEST)
            if not enrl_obj.exists():
                return Response({'success':False,'message':'User not registered in the hackathon'}, status=status.HTTP_400_BAD_REQUEST)
            if hackathon_obj.submission_type=="LINK":
                submission_obj = Submission.objects.create(hackathon=hackathon_obj, owner = request.user, type = hackathon_obj.submission_type, link=data['link'])
                seralialized_data = SubmissionSerializer(submission_obj).data
                return Response({'success':True,'message':'Successfully submitted','submission':seralialized_data}, status=status.HTTP_202_ACCEPTED)
            elif hackathon_obj.submission_type=="IMAGE":
                submission_obj = Submission.objects.create(hackathon=hackathon_obj, owner = request.user, type = hackathon_obj.submission_type, image_file =data['image_file'])
                seralialized_data = SubmissionSerializer(submission_obj).data
                return Response({'success':True,'message':'Successfully submitted','submission':seralialized_data}, status=status.HTTP_202_ACCEPTED)
            elif hackathon_obj.submission_type=="FILE":
                submission_obj = Submission.objects.create(hackathon=hackathon_obj, owner = request.user, type = hackathon_obj.submission_type, text_file =data['text_file'])
                seralialized_data = SubmissionSerializer(submission_obj).data
                return Response({'success':True,'message':'Successfully submitted','submission':seralialized_data}, status=status.HTTP_202_ACCEPTED)
        except KeyError:
            return Response({'success':False,'message':'Submission type invalid'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'success':False,'message':'Hackathon does not exist or submission period has expired'}, status=status.HTTP_400_BAD_REQUEST)