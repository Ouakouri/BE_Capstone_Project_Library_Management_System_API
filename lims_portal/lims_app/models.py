from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
    
#This model contains information about the user who borrowed the book, the date of borrowing, and the date of return:
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

class reader(models.Model):
    def __str__(self):
        return self.reader_name
    reference_id = models.CharField(max_length=255)
    reader_name = models.CharField(max_length=255)
    reader_contact = models.CharField(max_length=255)
    reader_address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)