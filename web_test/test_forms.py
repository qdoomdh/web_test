from django.test import TestCase
from django.core.exceptions import NON_FIELD_ERRORS
from books.factories import AuthorFactory, BookFactory
from books.forms import ReviewForm, BookForm

class ReviewFormTest(TestCase):  #testing our form validation is working
    def test_no_review(self):    #for review form checking  error rais if review is empty or lest than 300 char
        form = ReviewForm(data={    #create a review form and pass some data
            'is_favourite':False,   
        })

        #remove: print(form.is_valid())  #check if the form is valid
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code= 'required'))  #we can assert that the form has a particular error
        #* has_error method gives 2 argument,the field we checking and the error code

    def test_review_too_short(self):    #for review form checking  error rais if review is empty or lest than 300 char
        form = ReviewForm(data={    #create a review form and pass some data
            'is_favourite': False, 
            'review':"Too short!",  #pass some review info but not 300 character
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code='min_lenght')) #these codes match exactly the validation that we created on our form

class BookFormTest(TestCase):
    def setUp(self):
        self.author = AuthorFactory()
        self.book = BookFactory(title="MyNewBook", authors=[self.author,])

    def test_custom_validation_rejects_books_that_already_exist(self):
        form = BookForm(data={  #cerate a form
            'title': "MyNewBook",    #pass the title and the author to be exactly the same as the books that we just created
            'authors': [self.author.pk,],
        })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code="bookexists"))   #we don't want to check the particular field raising error,we want to check the form is raising what's called a NON_FIELD_ERRORS

    def test_custom_validation_accepts_new_book(self):
        new_author = AuthorFactory()
        form = BookForm(data={
            'title': "MyUniqueBook",
            'authors': [new_author.pk],
        })
    
        self.assertTrue(form.is_valid())