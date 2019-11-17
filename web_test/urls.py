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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views #for logout
from django.conf import settings
from django.urls import path, include, re_path
import debug_toolbar
from books.views import (AuthorList, AuthorDetail, BookDetail, books_list #importing book list from views.py
                         ,CreateAuthor,ReviewList,review_book) #review_books) delete the reveiw_books
urlpatterns = [
    #Auth
    path('logout', auth_views.logout,{'next_page': 'books'}, name='logout'), #for logout
    path('login', auth_views.login,{'template_name': 'login.html'}, name='login'),
    #Admin
    path('admin/', admin.site.urls),
    #custom 
    path('__debug__', include(debug_toolbar.urls)),
    path('', books_list, name="books"),
    path('authors/',AuthorList.as_view(),name="authors"),
    path('books/<int:pk>',BookDetail.as_view(),name="book-detail"), #(?P<pk>[-\w]+/)
    path('authors/add',login_required(CreateAuthor.as_view()),name="add-author"), #it must be above of the author-detail,the ability to create an author
    #because we want to url to first match author-add befor hits the regular expression underneath
    path('authors/<int:pk>',AuthorDetail.as_view(),name="author-detail"), #(?P<pk>[-\w]+/)
    #path('review/', review_books, name='review-books'), delete this
    path('review/', login_required(ReviewList.as_view()), name='review-books'), #for classed base view we msut do this
    path('review/<int:pk>', review_book, name='review-book'),   #becase it's a function base view we've done it in views.py
]

