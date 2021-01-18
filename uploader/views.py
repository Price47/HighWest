from django.shortcuts import render

from .upload_helpers import UploadHelper

def index(request):
    return render(request, 'jinja2/index.html')

def upload(request):
    errors = []

    if request.method == 'POST' and request.FILES['file']:
        for line in request.FILES['file']:
            x = line.decode().split('\t')
            err = UploadHelper(x).process_transaction()
            if err:
                transaction, error = err
                errors.append({'transaction': transaction, 'err': error})

    return render(request, 'jinja2/upload.html', {'errors': errors})

