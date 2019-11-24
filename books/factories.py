import factory
from .models import Author, Book
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class AuthorFactory(factory.django.DjangoModelFactory):
    '''
    Create An AUthor.
    '''
    class Meta:
        model = Author
    
    name= factory.Faker('name')

class UserFactory(factory.django.DjangoModelFactory):
    """
    Creates a standard User
    """
    class Meta:
        model=User
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = first_name
    password = make_password("test")

class BookFactory(factory.DjangoModelFactory):
    """
    Creates a book without a review
    """
    class Meta:
        model=Book
    title= factory.Faker("word")    #for book title

    @factory.post_generation #post generation hook for tell factory how to create a ManyToMany relationship with authors
    def authors(self, create, extracted , **kwargs): #define what would be happened after a bookfactory has created a fake object
        if not create:  #if we not using create method, do nothing
            return
        if extracted:   #if we use : add each of the authors we pass in, to a created factory,these are represented here as extracted
            for authors in extracted:
                self.authors.add(authors) #in django 2 we add SILKY_META = True in settings

class ReviewFactory(BookFactory):
    """
    Creates a book with review
    """
    review = factory.Faker('text',max_nb_chars = 400) #additional field associated with review,use faker to generate a fake piece of text with max char of 400
    date_reviewd = now()
    reviewed_by = factory.SubFactory(UserFactory) #Create a realtionship reviewfactory and user 
    #for foreignkey we setting a SubFactory and passing UserFactory as argument,every time we create a review factory a userfactory will also be created and bound to this factory