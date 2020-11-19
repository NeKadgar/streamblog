from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .models import Classifier
# Create your views here.

def send_classifier(request):
    file_location = 'file/classifier.xml'
    file = Classifier.objects.latest("id")
    print(file.document.path)
    path = file.document.path
    try:
        with open(path, 'r') as f:
            file_data = f.read()
        # sending response
        response = HttpResponse(file_data, content_type='application/xhtml+xml')
        response['Content-Disposition'] = 'attachment; filename="foo.xls"'

    except IOError:
        # handle file not exist case here
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response