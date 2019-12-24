from django.contrib.auth.models import UserManager, User, AbstractUser	#We import User OBJECT*
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.timezone import now
from django.dispatch import receiver


# Create your models here.
class Book(models.Model): #now we need the quality that books might have
	title = models.CharField(max_length=150) #this going to be stored as a string we must set maximum lenght to store
	authors = models.ManyToManyField("Author",related_name="books")
	review = models.TextField(blank = True, null=True)
	reviewed_by = models.ForeignKey(User, blank=True, null=True, related_name='review', on_delete=models.PROTECT) 
	#*about the above code:this is a many-to-one field,first argument is the model we want to map(relationship with)
	#we must also defin a elated name:a book would have one user who its revied by but a user may have many rewveiws. then we user reviews related name
	#**Note: in django 2 and upper you must takes an additional argument on_deleted wich have option: cascade,protect,set(),...
	date_reviewd = models.DateTimeField(blank = True, null=True)#it is stored as a date_time object *
	is_favourite = models.BooleanField(default=False,verbose_name="Favourite?")

	def __str__(self):
		return "{} by {}".format(self.title, self.list_authors())

	def list_authors(self):
		return "-".join([author.name for author in self.authors.all()])

	def save(self, *argv, **kwargv):
		if (self.review and self.date_reviewd is None):
			self.date_reviewd=now()
		super(Book,self).save(*args, **kwargs)

class Author(models.Model):
	name = models.CharField(max_length=70,help_text=' Use pen name,not Real name',
							 unique=True)
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):		#for returning author detail url
		return reverse('author-detail', kwargv={'pk', self.pk}) #takes url name and return url,and primary key of author

class UserProfile(AbstractBaseUser):
	#Requirmental
	username = models.CharField(
		max_length=30, 
		help_text=" at least 3 character. Letters, digits and @/./+/-/_ only.",
		unique=True,
		)
	email = models.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
	#Optional
	first_name = models.CharField(max_length = 100)
	last_name =  models.CharField(max_length = 100)
	address = models.TextField(blank=True, null=True )
	Phone = models.CharField(max_length = 50,help_text='write like this format: 09xxxxxxxx')
	birth_date = models.DateField(help_text= 'Format: YYYY-MM-DD',blank=True, null=True)
	password= None
	#Backend
	is_superuser = models.BooleanField(default=False, verbose_name='SuperUser?')#verbose_name='سوپر یوزر'
	create_date = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS= ['username', 'email']
	objects = UserManager()

	def __str__(self):
		return self.username

	# def save(self, *args, **kwargs):
	# 	if (self.last_login is None):
	# 		self.last_login = now()
	# 	super(UserProfile,self).save(*args, **kwargs)