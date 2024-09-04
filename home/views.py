from django.shortcuts import render
from art.models import Art


# Create your views here.
def home(request):
    if 'image_path' in request.session:
        del request.session['image_path']
    art_rectangular = Art.objects.filter(categories__name='Rectangular', is_published=True)
    art_circle = Art.objects.filter(categories__name='Circular (black & white)', is_published=True)
    art_digital_prints = Art.objects.filter(categories__name='Digital Prints', is_published=True)
    context = {
        'art_rectangular': art_rectangular, 
        'art_circle' : art_circle,
        'art_digital_prints' : art_digital_prints
    }
    return render(request, 'home/home.html', context=context)