from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

from embed_video.fields import EmbedVideoField

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


class Category(models.Model):

    name=models.CharField(max_length=200,unique=True)

    def __str__(self):
        return self.name
    
class Course(models.Model):

    title=models.CharField(max_length=200)

    description=models.TextField()

    price=models.DecimalField(decimal_places=2,max_digits=5)

    owner=models.ForeignKey(User,on_delete=models.SET_NULL,related_name="courses",null=True)

    is_free=models.BooleanField(default=False)

    picture=models.ImageField(upload_to="courseimages",null=True,blank=True,default="courseimages/default.png")

    thumbnail=EmbedVideoField()

    category_objects=models.ManyToManyField(Category)
    
    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

from django.db.models import Max

class Module(models.Model):

    title=models.CharField(max_length=200)

    course_object=models.ForeignKey(Course,on_delete=models.CASCADE,related_name="modules")

    order=models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
    def save(self,*args,**kwargs):

        max_order=Module.objects.filter(course_object=self.course_object).aggregate(max=Max('order'))

        self.order=max_order+1

        self.save()
    

    
# Lesson
# =>title
# =>module_object(FK)

class Lesson(models.Model):

    title=models.CharField(max_length=200)

    module_object=models.ForeignKey(Module,on_delete=models.CASCADE,related_name='lessons')

    video=EmbedVideoField(null=True)

    order=models.PositiveIntegerField()

    def __str__(self):
        return f"{self.module_object.title} + {self.title}"