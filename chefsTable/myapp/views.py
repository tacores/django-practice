from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse 
from .forms import BookingForm
from .models import Menu

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
    return render(request, 'home.html')

def book(request):
    return render(request, 'book.html')

def book_form(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form': BookingForm() }
    return render(request, 'book_form.html', context)

def menu(request):
    return render(request, 'menu.html')

def about(request):
    return render(request, 'about.html')

def about2(request):
    about_content = {'about': "Little Lemon is a family-owned Mediterranean restaurant, focused on traditional recipes served with a modern twist. The chefs draw inspiration from Italian, Greek, and Turkish culture and have a menu of 12–15 items that they rotate seasonally. The restaurant has a rustic and relaxed atmosphere with moderate prices, making it a popular place for a meal any time of the day."}
    return render(request, 'about.html', about_content)

def menu_model(request):
    menu_items = Menu.objects.all()
    items_dict = {'menu': menu_items}
    return render(request, 'menu_model.html', items_dict)
