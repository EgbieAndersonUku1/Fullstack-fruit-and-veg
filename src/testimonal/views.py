from django.shortcuts import render

from .forms.testimonial.testimonial_form import TestimonalForm
# Create your views here.


def reviews_section(request):
    return render(request, "account/testimonials/reviews-and-feedback.html")


def add_testimonial(request):
       
    if request.method == "POST":
        form = TestimonalForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = TestimonalForm()
        
    context = {
        "form": form
    }
    return render(request, "account/testimonials/add-testimonial.html", context=context)