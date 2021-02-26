from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from csv import reader
from django.contrib.auth.models import User


def userdata(request):
    with open('templates/csv/your_file.csv', 'r') as csv_file:
        csvf = reader(csv_file)
        data = []
        for username, password, *__ in csvf:
            user = User(username=username)
            user.set_password(password)
            data.append(user)
        User.objects.bulk_create(data)
    return JsonResponse('user csv is now working', safe=False)