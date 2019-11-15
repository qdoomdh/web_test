from django.urls import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404,render,redirect #for 404 error in review_book/s
from django.views.generic import DetailView,View #use for subclassess
from django.views.generic.edit import CreateView
from .forms import BookForm,ReviewForm #this use for review form in review-book function
from .models import Author, Book #book is an object
#from django.http import HttpResponse # importing resond we no use it we can ermove it

def books_list(request):
    #return HttpResponse(request.user.username,"<h1>this is a test</h1>, we could put anything here")#we could put every html tags
    """
    list the books that have reviews
    """
	
    books= Book.objects.exclude(date_reviewd__isnull=True).prefetch_related('authors') #for query our database
	
    context = {  # we must send the books variable to list.html with render and context only accept dictionary
        "books": books,
    }
	
    return render(request, "list.html", context)


class AuthorList(View):
    def get(self, request):
	
       # authors=Author.objects.all() #to find out all authors and return to our response
        authors=Author.objects.annotate( #count wich authors how many books have.
            published_books=Count('books')  
        ).filter(
			published_books__gt=0
		) #filter only authors that have at least 1 publish books 
		
        context= {
             "authors":authors, #this related with authors.html file for knows as authors
        } 
		
        return render(request, "authors.html", context)


class BookDetail(DetailView):
    model = Book
    template_name = "book.html"


class AuthorDetail(DetailView):
    model = Author
    template_name = "author.html"
#def review_books(request):#


class ReviewList(View):
    """
    List all of the books that we want to review.
    """
    def get(self, request):     
        books = Book.objects.filter(date_reviewd__isnull=True).prefetch_related('authors')
        
        context = {
            'books': books,
            'form': BookForm,
        }
        
        return render(request, "list-to-review.html", context)

    def post(self, request):    #define post method as same as if statement in functional view
        form = BookForm(request.POST)
        books = Book.objects.filter(date_reviewd__isnull=True).prefetch_related('authors') #he list of books render in the post request.

        if form.is_valid():
            form.save()		 #This will automatically map all of the fields to a model and save them in our database
            return redirect('review-books')

        context = {
            'form': form,
            'books': books,
        }

        return render(request, "list-to-review.html", context)	#render our shortcut


def review_book(request, pk):
    """
	Review an individual book
    """

    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
		# Process our form
        form = ReviewForm(request.POST) #bind the recquest to the form
		
        if form.is_valid(): 
            book.is_favourite = form.cleaned_data['is_favourite']    #clean the book information and replace it, provided by from 
            book.review = form.cleaned_data['review']
            book.save() #save the book

            return redirect('review-books')     #return to the review-books(attention to the urls.py in that part we define review_books name as review-books)
			
    else:
        form = ReviewForm

    context = {
        'book': book,
        'form': form,
    }
	
    return render(request, "review-book.html", context)


class CreateAuthor(CreateView):     #CREATE AN AUTHOR PAGE
    model = Author          #we model the author
    fields = ['name',]  #the fields that shown in create author page
    template_name = "create-author.html"     #the template name for that page

    def get_success_url(self):  #if the form submit is sucessfull:
        return reverse('review-books')      #redirect to url,use reverse shortcut again