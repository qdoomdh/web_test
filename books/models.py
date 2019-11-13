from django.urls import reverse
from django.db import models
from django.utils.timezone import now
# Create your models here.
class Book(models.Model): #now we need the quality that books might have
	title = models.CharField(max_length=150) #this going to be stored as a string we must set maximum lenght to store
	authors = models.ManyToManyField("Author",related_name="books")
	review = models.TextField(blank = True, null=True)
	date_reviewd = models.DateTimeField(blank = True, null=True)#it is stored as a date_time object *
	is_favourite = models.BooleanField(default=False,verbose_name="Favourite?")

	def __str__(self):
		return "{} by {}".format(self.title, self.list_authors())

	def list_authors(self):
		return "-".join([author.name for author in self.authors.all()])

	def save(self, *argv, **kwargv):
		if (self.review and self.date_reviewd is None):
			self.date_reviewd=now()
		super(Book,self).save(*argv, **kwargv)

class Author(models.Model):
	name = models.CharField(max_length=70,help_text=' Use pen name,not Real name',
							 unique=True)
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):		#for returning author detail url
		return reverse('author-detail', kwargv={'pk', self.pk}) #takes url name and return url,and primary key of author

