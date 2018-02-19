from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
from .models import Greeting
from . import qe
import os

# Create your views here.
def index(request):
    return render(request,'index.html')

def log(request):
    return render(request,'log.html')

# Features
def parseDocxFile(request):
    file = request.FILES['file']
    quickexam = qe.QuickExam(os.getcwd())
    result = quickexam.jieda_docx_wenjian(file,int(request.GET['p']))
    return JsonResponse(result,safe=False)

def searchText(request):
    wenben,yeshu = request.GET['s'],request.GET['p']
    if wenben:
        quickexam = qe.QuickExam(os.getcwd())
        result = quickexam.zhao_daan_an_wenben(wenben,int(yeshu))
        return JsonResponse(result,safe=False)

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

