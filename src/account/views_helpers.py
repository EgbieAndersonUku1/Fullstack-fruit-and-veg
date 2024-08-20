from django.shortcuts import render, redirect
from django.urls import reverse

from account.utils.converter import convert_decimal_to_float


def handle_form(request, form_class, session_key, next_url_name, template_name):
    initial_data = request.session.get(session_key, {})
    form = form_class(initial=initial_data)
    context = {"section_id": session_key}

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            if form.has_changed():
                request.session[session_key] = convert_decimal_to_float(form.cleaned_data)
            return redirect(reverse(next_url_name))
    
    context["form"] = form
    return render(request, template_name, context=context)


