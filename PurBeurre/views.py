
from django.shortcuts import render


def index(request):
    return render(request, 'templates/layouts/search.html')

def mentions(request):
    context = {
        'title': 'Mentions',
        'page_title': 'Mentions légales',}
    return render(request, 'templates/layouts/mentions.html', context=context)
