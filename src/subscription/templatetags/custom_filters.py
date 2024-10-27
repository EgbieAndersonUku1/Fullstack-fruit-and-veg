from django import template

register = template.Library()



@register.filter
def format_frequency(frequency):
    if frequency == 'd':
        return 'Daily'
    elif frequency == 'w':
        return 'Weekly'
    elif frequency == 'bw':
        return 'Bi-weekly'
    elif frequency == 'm':
        return 'Monthly'
    elif frequency == 'q':
        return 'Quarterly'
    return frequency.title() 