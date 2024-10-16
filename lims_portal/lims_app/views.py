from django.shortcuts import render
from django.contrib import admin
from django.http import  HttpResponse
from django.shortcuts import render,redirect
from .models import *
# Create your views here.

def home(request):
    return render(request,"home.html", context={'current_tab' : "home"})

def readers(request):
    return render(request,"readers.html", context={'current_tab' : "readers"})

def readers_tab(request):
    readers = reader.objects.all()
    return render(request, "readers.html", context={'current_tab' : "readers", 'readers' : readers})

def save_reader(request):
    reader_item = reader(
        reference_id=request.POST['reader_ref_id'],
        reader_name=request.POST['reader_name'],
        reader_contact=request.POST['reader_contact'],
        reader_address=request.POST['address'],
        active=True
    )
    reader_item.save()
    return redirect('/readers')



def save_student(request):
    student_name = request.POST['student_name']
    return render(request,"welcome.html",context={'student_name': student_name})
