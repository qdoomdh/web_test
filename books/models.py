from django.db import models
class Book(models.Model): #now we need the quality that books might have
	title = models.CharField(max_length=150) #this going to be stored as a string we must set maximum lenght to store
	author = models.CharField(max_length=70,help_text=' Use pen name,not Real name') #this going to be stored as a string
	review = models.TextField(blank = True, null=True)
	date_reviewd = models.DateTimeField(blank = True, null=True)#it is stored as a date_time object *
	is_favourite = models.BooleanField(default=False,verbose_name="Favourite?")

	def __str__(self):
		return self.title
# Create your models here.