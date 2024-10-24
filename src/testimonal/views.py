from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required

from .models import Testimonial, TestimonialMessages
from .forms.testimonial.testimonial_form import TestimonialForm
from  utils.send_emails_types import notify_admin_of_new_testimonial
# Create your views here.


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def reviews_section(request):
    return render(request, "account/testimonials/reviews-and-feedback.html")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def add_testimonial(request):
    
    # Retrieve only the 'is_approved' field for the testimonial created by the current user, if it exists.
    # This avoids loading the entire testimonial object and only fetches the 'is_approved' field.
    testimonial = Testimonial.objects.filter(author=request.user).values('is_approved').first()

    has_already_created_testimonial = testimonial is not None
    is_approved                     = testimonial['is_approved'] if testimonial else False
    
    if request.method == "POST":

        form = TestimonialForm(request.POST)
        
        if form.is_valid():
           ratings = int(request.POST.get("star-rating"))
           
           testimonal = Testimonial(
               author=request.user,
               job_title=form.cleaned_data["job_title"],
               user_image=form.cleaned_data["user_image"],
               testimonial_text=form.cleaned_data["testimonial_text"],
               ratings=ratings,
               company_name=form.cleaned_data["company_name"],
               country=form.cleaned_data["country"],
               location=form.cleaned_data["location"],
           )
        
           testimonal.save()
           messages.success(request, "You have successfully created a testimonial. We will let you know once your testimonial has been approved")
           
           is_sent = notify_admin_of_new_testimonial(user=request.user, 
                                                     subject="A newly created testimonial has being created an awaiting your approval")
           
           if is_sent:
               print("Email sent..")
           else:
               # Add logger here later to record why
               print("Email not sent...")
           return redirect("add-testimonial")
       
    else:
        form = TestimonialForm()
        
    context = {
        "form": form,
        "already_created": has_already_created_testimonial,
        "is_approved": is_approved,
        "is_editing": False,
    }
    return render(request, "account/testimonials/add-testimonial.html", context=context)


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def all_reviews(request):
    context = {}
    return render(request, "account/testimonials/review-section.html", context=context)


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def display_testimonial(request):
    
    testimonial = Testimonial.get_by_user(request.user)
    context     = {
        "testimonial": testimonial
    }
    return render(request, "account/testimonials/view-testimonial.html", context=context)


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def delete_testimonial(request, id):
    
    testimonial = Testimonial.get_by_user_and_id(request.user, id)
    if testimonial:
        testimonial.delete()
        messages.success(request, "Your testimonial was successfully deleted")
    else:
         messages.error(request, "Something went wrong and your testimonial wasn't deleted")
    return redirect("reviews")


@login_required(login_url=settings.LOGIN_URL, redirect_field_name='next')
def edit_testimonial(request, username, id):
    
    # Ensure the testimonial belongs to the logged-in user
    if request.user.username.lower() != username.lower():
        messages.error(request, TestimonialMessages.ERROR_EDITING_OTHER_TESTIMONIAL)
        return redirect("display_testimonial")
    
    testimonial = Testimonial.get_by_user_and_id(user=request.user, testimonial_id=id)
    
    if not testimonial:
        messages.error(request, TestimonialMessages.ERROR_TESTIMONIAL_NOT_FOUND)
        return redirect("display_testimonial")
    
    form = TestimonialForm(instance=testimonial)
    
    if request.method == "POST":
        form = TestimonialForm(request.POST, instance=testimonial)
        if form.is_valid():
            form.save(reset_fields=True)
            messages.success(request, TestimonialMessages.SUCCESS_TESTIMONIAL_UPDATED)
            return redirect("display_testimonial")
    
    context = {
        "form": form,
        "is_editing": True,
        "testimonial": testimonial,
        "already_created": False,
        "username": username,
        "is_approved": False,
        "id": id,
    }
    return render(request, "account/testimonials/add-testimonial.html", context=context)

