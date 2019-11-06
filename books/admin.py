from django.contrib import admin
from .models import Book,Author  #we can write from books.models import Book,Author
# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    fieldsets=[
        ("Book Details", {"fields": ["title", "authors"]}),
        ("Review", {"fields": ["is_favourite", "review", "date_reviewd"]} ),
     ]

    def book_authors (self, obj):
        return obj.list_authors()
        
#from here
    readonly_fields = ("date_reviewd",)
    list_display = ("title", "book_authors", "date_reviewd", "is_favourite")
    book_authors.short_description="author(s)"
    list_editable="is_favourite", #in the future add book_author and make it ok
    list_display_links = ("title","date_reviewd",)
    list_filter="is_favourite",#we can add another filter like->"date_reviewd",
    search_fields= ("title", "authors__name",)
#until here only set interface changes
admin.site.register(Author)