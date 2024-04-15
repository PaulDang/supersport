from django import template

register = template.Library()

@register.filter
def price_format(value):
    """Formats a number to currency with commas."""
    try:
        # Assuming value is a string or number
        value = float(value)
        return "{:,.0f} VNĐ".format(value)
    except ValueError:
        return value