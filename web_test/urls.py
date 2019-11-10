"""web_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
import debug_toolbar
from books.views import (AuthorList, AuthorDetail, BookDetail, books_list #importing book list from views.py
                         ,review_book, review_books) 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__', include(debug_toolbar.urls)),
    path('', books_list, name="books"),
    path('authors/',AuthorList.as_view(),name="authors"),
    path('books/<int:pk>',BookDetail.as_view(),name="book-detail"), #(?P<pk>[-\w]+/)
    path('authors/<int:pk>',AuthorDetail.as_view(),name="author-detail"), #(?P<pk>[-\w]+/)
    path('review/', review_books, name='review-books'),
    path('review/<int:pk>', review_book, name='review-book'),
]

