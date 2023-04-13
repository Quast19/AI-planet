from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from .constants import SUBMISSION_TYPE

# Create your models here.
def upload_to(instance, filename):
    return 'img/{filename}'.format(filename=filename)

class Hackathon(models.Model):
    hosted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    title = models.TextField()
    background_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    hackathon_image = models.ImageField(upload_to=upload_to, blank=True, null=True)
    submission_type = models.CharField(max_length=20, choices=SUBMISSION_TYPE, default='LINK')
    start_datetime = models.DateTimeField(default=timezone.now, editable=True)
    end_datetime = models.DateTimeField(blank=True)
    prize_amount = models.IntegerField()
    
    def get_bgimage_url(self):
        return request.build_absolute_uri(self.background_image)
    def get_hackathonimage_url(self):
        return request.build_absolute_uri(self.hackathon_image)
    # def save(self, *args, **kwargs):
    #     self.end_datetime = self.start_datetime + timedelta(days=1)
    #     super(Hackathon, self).save(*args, **kwargs)
    def __str__(self):
        return str(self.title) 

class Enrolment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(default=timezone.now, editable=False)
    def __str__(self):
        return str(self.user.username) + " " +str(self.hackathon.title) 