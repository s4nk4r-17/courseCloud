from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    ROLE_CHOICES=[
        ('Instructor','Instructor'),
        ('Student','Student'),
    ]

    role=models.CharField(max_length=20,choices=ROLE_CHOICES,default='Student')

class InstructorProfile(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")

    expertise=models.CharField(max_length=200,null=True)

    profile_picture=models.ImageField(upload_to="profilepics",null=True,blank=True,default="profilepics/default.png")

    about=models.CharField(max_length=200,null=True)

from django.db.models.signals import post_save
    
def create_instructor_profile(sender,instance,created,**kwargs):

    if created and instance.role=="Instructor":

        InstructorProfile.objects.create(owner=instance)

post_save.connect(create_instructor_profile,User)