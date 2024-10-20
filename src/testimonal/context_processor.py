from .models import Testimonial


def get_approved_testimonials(request) -> dict:
    """
    A context processor that allows the testimonial model 
    to be accessed in any template.
    
    The function retrieves all the approved testimonials
    and returns them in a dictionary.
    """
    try:
        approved_testimonials = Testimonial.get_approved_testimonials()
    except Exception as e:
         print(f"Error fetching approved testimonials: {e}")
         approved_testimonials = Testimonial.objects.none()
    
    return {
        "approved_testimonials": approved_testimonials  
    }
