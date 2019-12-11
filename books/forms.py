from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm #for usercreation register
from django.contrib.auth.models import User #for usercreation register

class ReviewForm(forms.Form):
    """
    form for reviewing the forms
    """

    is_favourite=forms.BooleanField(
        label="favourite?",
        help_text="In your top 100 book of all the time?",
        required=False,
    )
    review = forms.CharField(
        widget=forms.Textarea,
        min_length=300,
        error_messages={
            'required' :'Please enter your review',
            'min_length' :'Please write at least 300 characters.(you have written %(show_value)s)'
        }
    )
class BookForm(forms.ModelForm):
    class Meta:
        model= Book
        fields=['title','authors','reviewed_by'] #this fields directly same as the Book model
    
    def clean(self):
        #Super the clean method to maintain main validation and error message.
        super(BookForm, self).clean()

        try:
            title=self.cleaned_data.get('title')
            authors= self.cleaned_data.get('authors')
            review= self.cleaned_data.get(('reveiw'))
            for auth in authors:
                book = Book.objects.get(title=title,authors=auth ) #django 2.0 could not return list .though we must give[0] to the authors.

            raise forms.ValidationError(
            "The book {} by {} already exist".format(title,book.list_authors() ) #book.list_authors
        )
        except Book.DoesNotExist:
            return self.cleaned_data

class RegistrationForm(UserCreationForm):   #use for registration
    """
    this is a registration form, for creating new users.
    """
    first_name = forms.CharField(min_length=3,max_length=30, required=True, help_text= "Required")
    last_name = forms.CharField(min_length=3,max_length=30, required=False, help_text= "Optional.")
    email = forms.EmailField(max_length=200,help_text='Required. Use a valid email address.'  )
    

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name','username', 'email', 'password1','password2'
        )
        help_texts = {
            'password': "For strong password use at least 8 character including number,letters and sing",
            'username': 'Do Not forget your username',
        }
    