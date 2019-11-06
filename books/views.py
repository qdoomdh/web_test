from django.shortcuts import render
from .models import Book #book is an object
#from django.http import HttpResponse # importing resond we no use it we can ermove it

def books_list(request):
    #return HttpResponse(request.user.username,"<h1>this is a test</h1>, we could put anything here")#we could put every html tags
    '''
    list the books that have reviews
    '''
    books= Book.objects.exclude(date_reviewd__isnull=True).prefetch_related('authors') #for query our database
    contex = {  # i don't know why we make this
        "books": books,
    }
    return render(request, "list.html", contex)
#only one command should work here