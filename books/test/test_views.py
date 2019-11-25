from django.test import TestCase
from django.urls import resolve, reverse #change the django.core.urlresolvers to the django.url in django2
from books.models import Book
from books.views import books_list, ReviewList  #for ReviewList class base views	
from books.factories import AuthorFactory, ReviewFactory, BookFactory,UserFactory

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


class TestReviewList(TestCase):
    def setUp(self):
        self.user = UserFactory(username="test")
        self.author = AuthorFactory()

    def test_reviews_urls(self):    #check out our url
        url = resolve('/review/')   #resolve /review
        self.assertEqual(url.func.__name__, ReviewList.__name__) #for class base views want to access the name of function,and our view

    def test_authentication_control(self):
        #check unauthenticated user that can not view the pages.
        response = self.client.get(reverse('review-books'))  #pass the name of the view that we want to see
        #print(response.status_code) #what static_code we get when we visit page with unauthenticated user.
        self.assertEqual(response.status_code, 302)  #assert our respons.status_code = 302

        self.client.login(username='test', password='test')  #check what happend when we have authenticated user
        response = self.client.get(reverse('review-books'))
        self.assertEqual(response.status_code,200)

        #While we're here, confirm we're using correct template
        self.assertTemplateUsed(response, 'list-to-review.html')
    
    def test_review_list_returns_books_to_review(self):
        #Setup our data
        # move this code  to setup author = AuthorFactory()    #create some author
        books_without_reviews = BookFactory.create_batch(2, authors=(self.author,))  #create books_without_reviews with bookfactory

        self.client.login(username='test', password='test') #login`
        response = self.client.get(reverse('review-books')) #get the veiw

        books = list(response.context['books']) # build a list of each of the books in our context
        self.assertEqual(books, books_without_reviews)
    
    def test_can_create_new_book(self):
        self.client.login(username='test', password='test') #login ourself in
        response = self.client.post(
            reverse ('review-books'),   #first argument :reverse a view
            data={         #passing some data
                'title':"My Brand New Book",
                'author':[self.author.pk],   #we can reuse it here again(from AuthorFactory.create_batch,
                    #above code: our form is expecting the primarykey of the object rather than the object itself
                'reviewed_by':self.user.pk,  #i'm going to say it's reviewed_by our user
            },
        )

        # remove: print (Book.objects.get(title="My Brand New Book"))  #See whetere or not this book is being saved to database,use get to book object
        self.assertIsNotNone(Book.objects.get(title="My Brand New Book"))	#check that the object exist