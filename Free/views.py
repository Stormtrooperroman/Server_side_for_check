from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django import forms
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from Free.tester import main


# Create your views here.

class FileFieldForm(forms.Form):

    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))


class HttpResponseThen(HttpResponse): 

    def __init__(self, data, arg, then_callback=lambda: 'hello world', **kwargs):
        super().__init__(data, **kwargs)
        self.then_callback = then_callback
        self.arg = arg

    def close(self):
        super().close()
        self.then_callback(self.arg)


@csrf_exempt
def index(request):
    template = loader.get_template('Free/index.html')
    return HttpResponse(template.render())

@csrf_exempt
def work_with_file(request):
    
    if request.method == 'POST':
        form = FileFieldForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        data = []
        if form.is_valid():
            for f in files:
                data.append(handle_uploaded_file(f))
           
            
            return HttpResponseThen("Ok", then_callback=work_with_data, arg = data)

def handle_uploaded_file(f):
    data = ""
    for chunk in f.chunks():
        data+=chunk.decode("utf-8")
    
    return data

def work_with_data(files):
    print(files)
    main()


def room(request, room_name):
    print("Ok man loch")

