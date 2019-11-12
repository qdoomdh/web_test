from django.shortcuts import get_object_or_404,render,redirect #for 404 error in review_book/s
from django.db.models import Count
from .forms import ReviewForm #this use for review form in review-book function
from .models import Book,Author #book is an object
from django.views.generic import DetailView,View #use for subclassess
#from django.http import HttpResponse # importing resond we no use it we can ermove it

def books_list(request):
    #return HttpResponse(request.user.username,"<h1>this is a test</h1>, we could put anything here")#we could put every html tags
    '''
    list the books that have reviews
    '''
    books= Book.objects.exclude(date_reviewd__isnull=True).prefetch_related('authors') #for query our database
    contex = {  # we must send the books variable to list.html with render and context only accept dictionary
        "books": books,
    }
    return render(request, "list.html", contex)

class AuthorList(View):
    def get(self, request):
        authors=Author.objects.all() #to find out all authors and return to our response
        authors=Author.objects.annotate( #count wich authors how many books have.
            published_books=Count("books")  
        ).filter(published_books__gt=0) #filter only authors that have at least 1 publish books 
        contex= {
             "authors":authors, #this related with authors.html file for knows as authors
        }
        return render(request, "authors.html", contex)

class BookDetail(DetailView):
    model=Book
    template_name="book.html"
class AuthorDetail(DetailView):
    model=Author
    template_name="author.html"

def review_books(request):
	"""
	List all of the books that we want to review.
	"""
	books = Book.objects.filter(date_reviewd__isnull=True).prefetch_related('authors')
	
	context = {
		'books': books,
	}
	
	return render(request, "list-to-review.html", context)

def review_book(request, pk):
    '''
	Review an individual book
    '''

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST) #bind the recquest to the form
        if form.is_valid(): 
            book.is_favourite= form.cleaned_data['is_favourite']    #clean the book information and replace it, provided by from 
            book.review=form.cleaned_data['review']
            book.save() #save the book

            return redirect("review-books")     #return to the review-books(attention to the urls.py in that part we define review_books name as review-books)
    else:
        form=ReviewForm

    contex={
        'book':book,
        'form':form,
    }
    return render(request, 'review-book.html', contex)