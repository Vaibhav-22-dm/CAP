from django.db import models
from AbstractUserModel.models import MyUser
# Create your models here.
class ead_Participant(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)
    college = models.CharField(max_length=20, null=True, blank=True)
    # ambassador = models.ForeignKey(MyUser, null=True, blank=True, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, null=True, blank=True)
    def __str__(self):
        return self.name