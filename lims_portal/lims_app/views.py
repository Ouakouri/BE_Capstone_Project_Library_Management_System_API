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
    if request.method=="GET":
        readers = reader.objects.all()
        return render(request, "readers.html", context={'current_tab' : "readers", 'readers' : readers})
    else:
        query = request.POST['query']
        readers = reader.objects.raw("select * from lims_app_reader where reader_name like '%"+query+"%'")
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

# fonctions for books page:

def books(request):
    return render(request,"books.html", context={'current_tab' : "books"})

def books_tab(request):
    if request.method=="GET":
        books = reader.objects.all()
        return render(request, "books.html", context={'current_tab' : "books", 'books' : books})
    else:
        query = request.POST['query']
        books =  Book.objects.raw("select * from lims_app_Book where title like '%"+query+"%'")
        return render(request, "books.html", context={'current_tab' : "books", 'books' : books})


def save_book(request):
    book_item = Book(
        title=request.POST['title'],
        author=request.POST['author'],
        isbn=request.POST['isbn'],
        published_date=request.POST['published_date'],
        copies_available=request.POST['copies_available'],
        active=True
    )
    book_item.save()
    return redirect('/books')

