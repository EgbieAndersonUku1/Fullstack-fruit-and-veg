from django.shortcuts import render

# Create your views here.


def blog_home_page(request):
    return render(request, "blog/index.html")


def blog_details(request, blog_id=1):
    
    return render(request, "blog/blog_details.html")