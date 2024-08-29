from django.shortcuts import render

from authentication.forms.register_form import RegisterForm
from authentication.forms.login_form import LoginForm


# Create your views here.

def index(request):
    return render(request, "index.html", 
                  context={"register_form": RegisterForm(),
                           "login_form": LoginForm()}
                  
                  )



