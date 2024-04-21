from django.shortcuts import render
from django.http import HttpResponse
from .models import Work

# Create your views here.
def home(request):
    works = Work.objects.all()
    return render(request, 'base/home.html', {'works': works})

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    return render(request, 'base/contact.html')
