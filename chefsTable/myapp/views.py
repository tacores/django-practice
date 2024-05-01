from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from .forms import BookingForm

def index(request): 
    return HttpResponse("Hello, world. This is the index view of MyApp.") 

def drinks(request, drink_name):
    d = {'mocha': 'type of coffee',
         'tea': 'type of beverage',
         'lemonade': 'type of refreshment',
         }
    choise_of_drink = d[drink_name]
    return HttpResponse(f'''<h2> {drink_name} </h2>
                        {choise_of_drink}''')

def home(request):
    return HttpResponse('Welcome to Little Lemon!')

def about(request):
    return HttpResponse('About us')

def menu(request):
    return HttpResponse('Menu')

def book(request):
    return HttpResponse('Make a booking')

def book_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': BookingForm() }
    return render(request, 'book_form.html', context)
