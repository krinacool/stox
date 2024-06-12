from django.shortcuts import render,redirect
from home.models import *

# Create your views here.
def trends(request):
    news = News.objects.all()
    ca = CA.objects.all()
    context = {
        "news":news,
        "ca":ca,
    }
    return render(request,'trends.html',context)