from django import template
import re

register = template.Library()

@register.simple_tag
def to_int(value, dlevery):
    value1= float(value)
    value2= float(dlevery)
    total= value1+value2
    return total

@register.filter()
def persentis(was,current):
	wasprice= float(was)
	currentprice= float(current)
	minus= int(wasprice-currentprice)
	musti= int(minus*100)
	result= int(musti/wasprice)
	return(result)

@register.filter
def replace_to_webp(value):
    """
    Custom filter to replace .png, .jpg, and .jpeg extensions with .webp.
    Usage: {{ value|replace_to_webp }}
    """
    if isinstance(value, str):
        # Ensure the value is a valid URL or path
        return re.sub(r'\.(png|jpg|jpeg)$', '.webp', value, flags=re.IGNORECASE)
    return value  # Return the original value if it's not a string
