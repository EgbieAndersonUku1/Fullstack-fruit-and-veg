from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Testimonial
from .forms.testimonial.testimonial_form import TestimonalForm
from  authentication.utils.send_emails_types import notify_admin_of_new_testimonial
# Create your views here.


def reviews_section(request):
    return render(request, "account/testimonials/reviews-and-feedback.html")


def add_testimonial(request):
    
    # Retrieve only the 'is_approved' field for the testimonial created by the current user, if it exists.
    # This avoids loading the entire testimonial object and only fetches the 'is_approved' field.
    testimonial = Testimonial.objects.filter(author=request.user).values('is_approved').first()

    has_already_created_testimonial = testimonial is not None
    is_approved = testimonial['is_approved'] if testimonial else False
    
    
    if request.method == "POST":

        form = TestimonalForm(request.POST)
        
        if form.is_valid():
           ratings = int(request.POST.get("star-rating"))
           
           testimonal = Testimonial(
               author=request.user,
               title=form.cleaned_data["title"],
               user_image=form.cleaned_data["user_image"],
               testimonial_text=form.cleaned_data["testimonial_text"],
               ratings=ratings,
               company_name=form.cleaned_data["company_name"],
               country=form.cleaned_data["country"],
               location=form.cleaned_data["location"],
           )
           
           testimonal.save()
           messages.success(request, "You have successfully created a testimonial. We will let you know once your testimonial has approved")
           
           is_sent = notify_admin_of_new_testimonial(user=request.user, subject="A newly created testimonial has being created an awaiting your approval")
           
           if is_sent:
               print("Email sent..")
           else:
               # Add logger here later to record why
               print("Email not sent...")
           return redirect("add-testimonial")
       
    else:
        form = TestimonalForm()
        
    context = {
        "form": form,
        "already_created": has_already_created_testimonial,
        "is_approved": is_approved,
    }
    return render(request, "account/testimonials/add-testimonial.html", context=context)