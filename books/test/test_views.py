from django.test import TestCase
from django.urls import resolve, reverse #change the django.core.urlresolvers to the django.url in django2
from books.views import books_list
from books.factories import AuthorFactory, ReviewFactory, BookFactory

class TestListBook(TestCase):
    def test_list_book_url(self):   #check the url behaves as we expect
        url = resolve("/") #resolve a string,something we expected that the user to type in(/ for example)because we are cheking the root url
        self.assertEqual(url.func, books_list) #chek the function associated with that resolve url, matches our books view
    
    def test_list_books_template(self):
        response = self.client.get(reverse(books_list)) #this is using testcase builtin client to make a get request,get the reverse of url
        self.assertTemplateUsed(response , "list.html") #check that the list.html which is the template we specify in our view is acctually serving this page.

    def list_books_returns_books_with_review(self):
        #Setup our data
        author = AuthorFactory() #Create an author
        books_with_reviews = ReviewFactory.create_batch(2, authors= [author,]) 	#use the ReviewFactory to create a bach of 2 books where the authors = my author
        #Now authors takes a lists,so in this case we passing author object inside a list
        books_without_review = ReviewFactory.create_batch(4, authors=[author,])

        response = self.client.get(reverse(books_list)) #get a view ,from the response we want to get a list of books in the context
        books = list(response.context['books']) #we define this in view itself so we've create a list of the books that have been returned

        self.assertEqual(books_with_reviews, books) #asserting books_with_reviews matching a books
        self.assertNotEqual(books_without_review, books) #asserting books_without_reviews dosen't match the books