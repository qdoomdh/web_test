from django.shortcuts import render
from django.http import HttpResponse # importing resond

def books_list(request):
    return HttpResponse(request.user.username,"<h1>this is a test</h1>, we could put anything here")#we could put every html tags
#only one command should work here