from django.http import HttpResponse
from django.template import loader

def cart(request):
  template = loader.get_template('cart.html')
  return HttpResponse(template.render())

def main(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())