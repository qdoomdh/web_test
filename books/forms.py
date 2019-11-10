from django import forms

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