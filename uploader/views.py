from django.shortcuts import render

def index(request):
    return render(request, 'jinja2/index.html')

def upload(request):
    return render(request, 'jinja2/upload.html')

