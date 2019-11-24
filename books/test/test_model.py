from django.test import TestCase
from books.factories import AuthorFactory
from books.models import Book
#rename tests.py into test_model.py
#Create your code here
class BookTest(TestCase):   #rename Demo test to BookTest  #for creating author in authorfactory
    def setUp(self): #setup run directly befor each test in testcase, notice capitalize of setUp it's important
        self.author1 = AuthorFactory(name= "Author 1") #call our first author author1 and overwrite the name
        self.author2 = AuthorFactory(name= "Author 2")

        self.book = Book(title="My book")   #create an object instead call factory
        self.book.save()
        self.book.authors.add(self.author1.pk, self.author2.pk) #add both of our authors to an instance,we need pass the primarykey for both of objects.
    
    def tearDown(self): #from this to upper is the foundation for a test
        self.author1.delete()
        self.author2.delete()
        self.book.delete()

    def test_can_list_authors(self): #first testcase,test each of the method on book#check wheter or not we can list our authors
        self.assertEqual("Author 1-Author 2", self.book.list_authors())  #assert that when called list_authors method,we get return author1 , author2
        #this is important:Author 1-author 2 the dash(-) is so important in this way
    #def test_addition(self):
     #   self.assertEqual(1 + 1, 2)  #right code
        #self.assertEqual(1 + 1, 3) #wrong code
    def test_string_method(self):
        self.assertEqual("My book by Author 1-Author 2", self.book.__str__()) ##equals the string in book to the first thing we wrote(MyBook by Author 1 ,..)
    
    def test_custom_save_method(self):
        self.assertIsNone(self.book.date_reviewd) #check we do not have date_reviewed record on our book
        self.book.review = "My review" #create a review
        self.book.save()    	#call our/a custom save method
        self.assertIsNotNone(self.book.date_reviewd) #check that because of our save method has been called,that the date_reviewed field has been filled