from distutils import extension
from django import template
from django.template.defaultfilters import stringfilter, stringformat
import markdown as md

register = template.Library()


@register.simple_tag()
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0]!=field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
        
    return url


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code'])

