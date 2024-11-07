from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .forms import NewBlogPost
from utils.decorators import is_authorised

# Create your views here.


def blog_home_page(request):
    return render(request, "blog/index.html")


def blog_details(request, blog_id=1):
    return render(request, "blog/blog_details.html")


@is_authorised
@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def blog_section(request):
    return render(request, "blog/manage_blogs.html")



@is_authorised
@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def create_blog_post(request):
    new_post = NewBlogPost()
    context  = {
        "form": new_post
    }
    return render(request, "blog/new_post.html", context=context)