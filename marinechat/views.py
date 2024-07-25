from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from django.urls import reverse

import json

from .models import Message, User
from .utils import retrieve_and_generate


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    return render(request, "marinechat/index.html", {
        'messages': Message.objects.filter(user=request.user)
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "marinechat/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "marinechat/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "marinechat/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "marinechat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "marinechat/register.html")

def documents(request):
    return render(request, 'marinechat/documents.html')

def query(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        message = data.get("query", "")
        user = request.user
        reply = retrieve_and_generate(message)

        msg_object = Message(sender='user', message=message, user=request.user)
        msg_object.save()
        rply_object = Message(sender='chatbot', message=reply, user=request.user)
        rply_object.save()

        response = serializers.serialize('json', Message.objects.filter(user=request.user))

        return JsonResponse({
            'messages': response,
        }, status=200)

    response = serializers.serialize('json', Message.objects.filter(user=request.user))

    return JsonResponse({
        'messages': response,
        'error': 'Method Not Allowed. Only POST method is allowed.'
    }, status=405)
