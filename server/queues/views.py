from django.contrib.auth import login
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    return render(request, 'index.html', context)


def room(request, room_name):
    context = {'room_name':room_name}
    return render(request, 'queue.html', context)