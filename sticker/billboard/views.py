from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .form import MessageForm, ConfigurationForm
from .models import Message





def billboard(request):
    bills = Message.objects.all()
    context = {'bills': bills}

    return render(request, 'billboard/message.html', context)


def create_message(request):
    form = MessageForm(request.POST, request.FILES)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('billboard')
    return render(request, 'billboard/message_form.html', context)


def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    message.delete()
    return redirect('billboard')


def add_config(request):
    form = ConfigurationForm(request.POST)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('create_message')
    return render(request, 'billboard/config.html', context)
