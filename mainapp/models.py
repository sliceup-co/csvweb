from django.db import models
import random
import time

def generate_pk():
    number = random.randint(1, 999)
    return 'J{}{}'.format(int(time.time()), number)


def job_directory_path(instance, filename):
    return 'inputs/job_{0}'.format(filename)

class Job(models.Model):
    jobid = models.CharField(default=generate_pk, primary_key=True, max_length=255, unique=True)
    email=models.EmailField(blank=False)
    check_terms=models.BooleanField(default=True)

class JobFile(models.Model):
    job = models.OneToOneField(Job,on_delete=models.CASCADE,primary_key=True)
    file = models.FileField(upload_to=job_directory_path)
