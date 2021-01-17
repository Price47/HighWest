from django.shortcuts import render

from .upload_helpers import UploadHelper

def index(request):
    return render(request, 'jinja2/index.html')

def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        for line in request.FILES['file']:
            x = line.decode().split('\t')
            UploadHelper(x).process_transaction()

    return render(request, 'jinja2/upload.html')

