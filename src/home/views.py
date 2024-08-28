from django.shortcuts import render

from authentication.forms.register_form import RegisterForm
# Create your views here.

def index(request):
    return render(request, "index.html", context={"form": RegisterForm()})

