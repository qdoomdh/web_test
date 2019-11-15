from django import forms
from .models import Book

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
        fields=['title','authors']
    
    def clean(self):
        #Super the clean method to maintain main validation and error message.
        super(BookForm, self).clean()

        try:
            title=self.cleaned_data.get('title')
            authors= self.cleaned_data.get('authors')
            review= self.cleaned_data.get('reveiw')
            book = Book.objects.get(title=title,authors=authors[0] ) #django 2.0 could not return list .though we must give[0] to the authors.
            
            raise forms.ValidationError(
            "The book {} by {} already exist".format(title,book.list_authors() ) #book.list_authors
        )
        except Book.DoesNotExist:
            return self.cleaned_data
