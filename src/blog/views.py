from django.shortcuts import render

# Create your views here.


def blog_home_page(request):
    return render(request, "blog/index.html")