from django.shortcuts import render

def index(request):
    return render(request, 'jinja2/index.html')

