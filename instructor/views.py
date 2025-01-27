from django.shortcuts import render
from django.views.generic import View
from instructor.forms import InstructorCreateForm
# Create your views here.


class InstructorCreateView(View):

    def get(self,request,*args,**kwargs):

        form_instance=InstructorCreateForm()

        return render(request,'instructor_register.html',{'form':form_instance})