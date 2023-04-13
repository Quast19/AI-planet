from django.db import models
from django.contrib.auth.models import User
import uuid
from hackathon.models import Hackathon, Enrolment
from django.utils import timezone
from hackathon.constants import SUBMISSION_TYPE
from django.core.exceptions import ValidationError

# Create your models here.
def username_path(instance, filename):
    return '{0}/user_{1}/{2}_{3}'.format(instance.hackathon.submission_type, instance.owner.username, instance.hackathon.title, filename)

class Submission(models.Model):
    is_valid = False
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    hackathon = models.ForeignKey(Hackathon,on_delete=models.CASCADE)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    type = models.CharField(max_length=20, choices=SUBMISSION_TYPE, default='LINK')
    updated_at = models.DateTimeField(auto_now=True)
    text_file = models.FileField(upload_to =username_path,blank=True, null=True)
    link = models.CharField(max_length=256,blank=True, null=True)
    image_file = models.ImageField(upload_to=username_path, blank=True, null=True)
    
    def __str__(self):
        return str(self.owner.username) + " " +str(self.hackathon.title) + "-" +str(self.id)
    
    def clean(self):
        self.is_valid = True
        if self.hackathon.submission_type!=self.type:
            raise ValidationError("a Submission format invalid !")
        if self.type=="LINK" and self.link is None and self.text_file is not None and self.image_file is not None:
            raise ValidationError("b Submission format invalid !")
        elif self.type=="IMAGE" and self.image_file is None and self.text_file is not None and self.link is not None:
            raise ValidationError("c Submission format invalid !")
        elif self.type=="FILE" and self.text_file is None and self.link is not None and self.image_file is not None:
            raise ValidationError("d Submission format invalid !")
        super(Submission, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_valid:
            self.full_clean()
        super(Submission, self).save(*args, **kwargs)
