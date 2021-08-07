import os
import time
import shutil
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse ,FileResponse
from subprocess import Popen, PIPE
from django.conf import settings
from .models import Job,JobFile
from django import forms
from django.core.exceptions import ValidationError


def download_files(request,jobid):
    filename="mainapp/media/output/Book1.xlsx"
    # filename="mainapp/media/output/job_"+str(jobid)+'.xlsx'
    response = HttpResponse(open(filename, "rb"), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename=job_{}.xlsx'.format(jobid)
    return response


def file_size(value): # add this to some file where you can import it from
    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MB.')

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[file_size])
    email=forms.EmailField()
    check_terms = forms.BooleanField(label="Accept Terms and Conditions")

# Create your views here.
def home(request):
    form = UploadFileForm()
    return render(request,'index.html',{'form':form})

def newjob(request):
    if request.method=="POST":
        start_time = time.time()
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if not form.is_valid():
            return JsonResponse({"error":"File too large. Size should not exceed 5 MB."})
        if form.is_valid():
            #saving Job model first
            inst=Job(email=request.POST["email"],check_terms=request.POST['check_terms'])
            inst.save()
            #saving jobfile model after creating job in order to get primary key of job
            instance = JobFile(job=inst,file=request.FILES['file'])
            instance.save()
            time.sleep(5)

            # infile="media/inputs/job_{0}.star".format(inst.jobid)
            # main_command="python log_sender_mike.py -i "+infile+" 
            # p = Popen([main_command], shell=True,cwd="mainapp",stdout=PIPE, stderr=PIPE)
            # out, err = p.communicate()
            # if err:
            #     print(err)
            #     return JsonResponse({"error":"Could Not run the Job! Maybe Some error in inputs"})
            context={
            "email":inst.email,
            "jobid":inst.jobid,
            "time_taken":int(time.time() - start_time) 
            }
            return JsonResponse(context)
        else:
            return JsonResponse({"error":"File Inputs May be wrong"})
    return JsonResponse({"error":"Form is not valid"})

def deletejob(request,jobid):
    try:
        file_name='mainapp/media/output/job_'+jobid+'.xlsx'
        os.remove(file_name)
        return HttpResponse({'msg':"File Deleted Sucessfully"})
    except Exception as e:
        return JsonResponse({'error':"File not found"})
    return JsonResponse({"error":"Form is not valid"})

