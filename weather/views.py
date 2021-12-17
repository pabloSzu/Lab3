import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def index(request):
    
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=769b2e5a52dd401a271875251618bd30&lang=es'

    err_msg = ''
    message = ''
    message_class = ''
    total = 0
    count = 0

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Ciudad no existente en el mundo!'
            else:
                err_msg = 'La ciudad ya ha sido cargada!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Ciudad cargada correctamente!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()
        
        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

        total += r['main']['temp']

        count += 1
    
    if count == 0:
        count = 1

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class,
        'total' : round(total/count,2)
    }


    return render(request, 'weather/weather.html', context)



def home_fahrenheit(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=769b2e5a52dd401a271875251618bd30&lang=es'


    err_msg = ''
    message = ''
    message_class = ''
    total = 0
    count = 0

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Ciudad no existente en el mundo!'
            else:
                err_msg = 'La ciudad ya ha sido cargada!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'Ciudad cargada correctamente!'
            message_class = 'is-success'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

        total += r['main']['temp'] 

       
        count += 1
    
        
    if count == 0:
        count = 1

    context = {
        'weather_data' : weather_data, 
        'form' : form,
        'message' : message,
        'message_class' : message_class,
        'total' : round(total/count,2)
    }


    return render(request, 'weather/weather_fahrenheit.html', context)







def home_detalle(request):
    url_with_fahrenheit = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=769b2e5a52dd401a271875251618bd30&lang=es'
    url_with_celcius =  'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=769b2e5a52dd401a271875251618bd30&lang=es'

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        r = requests.get(url_with_fahrenheit.format(city)).json()
        r_c = requests.get(url_with_celcius.format(city)).json()

        city_weather = {
            'city' : city.name,
            'country': r['sys']['country'],
            'temperature_celcius' : r_c['main']['temp'],
            'temperature_f' : r['main']['temp'] ,
            'description' :  r['weather'][0]['description'].capitalize(),
            'icon' : r['weather'][0]['icon'],

            'wind' : r['wind']['speed'],
            
            'sensacion_term' : r['main']['feels_like'] ,
            'temperature_max_f' : r['main']['temp_max'] ,
            'temperature_min_f' : r['main']['temp_min'] ,
            'temperature_max_c' : r_c['main']['temp_max'],
            'temperature_min_c' : r_c['main']['temp_min'],
            'humedad' : r['main']['humidity'] ,
        }

        weather_data.append(city_weather)



    context = {
        'weather_data' : weather_data
    }


    return render(request, 'weather/weather_detalle.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    
    return redirect('home')

