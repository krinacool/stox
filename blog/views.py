from django.shortcuts import render

# Create your views here.
def startmarket(request):
    return render(request,'startmarket.html')

def whatsapp(request):
    return render(request,'whatsapp.html')

def email(request):
    return render(request,'email.html')