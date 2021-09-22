import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from config import API_TOKEN_


def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    message_text = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            if City.objects.filter(name=new_city).count() == 0:
                form.save()

                message_text = 'City successfully added'
                message_class = 'is-success'
            else:
                message_text = 'City already added'
                message_class = 'is-danger'

    form = CityForm()

    cities = City.objects.all()

    weather_data = []
    for city in cities:
        response = requests.get(url.format(city.name, API_TOKEN_)).json()

        city_weather = {
            'city': city.name,
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {
        'weather_data': weather_data,
        'form': form,
        'message_text': message_text,
        'message_class': message_class,
    }

    return render(request, 'weather/index.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')
