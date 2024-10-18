from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import admin
from django.http import  HttpResponse
from django.utils import timezone
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


# Create (Add new user)
def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user_profile = UserProfile(user=user)
        user_profile.save()
        return redirect('user_list')
    return render(request, 'add_user.html')

# Read (View all users)
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

# Update (Edit user data)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.save()
        user.userprofile.active = request.POST.get('active', False)
        user.userprofile.save()
        return redirect('user_list')
    return render(request, 'edit_user.html', {'user': user})

# Delete (Delete User)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')

# When trying to borrow a book, check to see if there are copies available. If there are, reduce the number:
def checkout_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.copies_available > 0:
        Transaction.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()
        return HttpResponse("Book checked out successfully")
    else:
        return HttpResponse("No copies available")
    
#When trying to borrow a book, check to see if there are copies available. If there are, reduce the number:
def checkout_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.copies_available > 0:
        Transaction.objects.create(user=request.user, book=book)
        book.copies_available -= 1
        book.save()
        return HttpResponse("Book checked out successfully")
    else:
        return HttpResponse("No copies available")

#When you return the book, update the record and add the return date:
def return_book(request, transaction_id):
    transaction = Transaction.objects.get(id=transaction_id)
    if not transaction.return_date:
        transaction.return_date = timezone.now()
        transaction.save()
        book = transaction.book
        book.copies_available += 1
        book.save()
        return HttpResponse("Book returned successfully")
    else:
        return HttpResponse("Book has already been returned")

#API endpoint to display available books, making sure to filter results by books that have copies available:
def available_books(request):
    books = Book.objects.filter(copies_available__gt=0)
    return render(request, "available_books.html", {'books': books})

