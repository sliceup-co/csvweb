from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse ,FileResponse
from subprocess import Popen, PIPE
from django.conf import settings


def download_image(request,image_name): 
    img=settings.MEDIA_ROOT +'/'+ image_name
    img_file = open(img, 'rb')
    response = FileResponse(img_file) 
    response['Content-Disposition'] = "attachment; filename=%s" % image_name
    return response





# Only needed if user is given to upload files of their own
from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

def handle_uploaded_file(f):
    with open('mainapp/tempfile.star', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Create your views here.
def home(request):
    image_data=None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
        clust_num=request.POST.get('cluster_num')
        infile='tempfile.star'
        main_command="python chep.py -i "+infile+" -c "+str(clust_num)
        p = Popen([main_command], shell=True,cwd="mainapp",stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        if out:
            image_data=infile.split('.')[0]+".chep_k"+str(clust_num)+".jpg"
            return render(request,'home2.html',{"infile":infile,"clust_num":clust_num,
            "image_data":image_data})
        else:
            return HttpResponse({'Error':err})
    else:
        form = UploadFileForm()
        return render(request,'home2.html',{'form':form})
