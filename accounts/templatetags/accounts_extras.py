from django import template

register = template.Library()

@register.simple_tag
def my_url(value, field_name, urlencode=None):
  url = '?{}={}'.format(field_name, value)

  if urlencode:
    query_string = urlencode.split('&')
    filtered_query_string = filter(lambda x: x.split("=")[0]!=field_name, query_string)
    encoded_querystring = '&'.join(filtered_query_string)
    url = '{}&{}'.format(url, encoded_querystring)
  
  return url