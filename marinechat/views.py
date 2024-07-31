from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json
import re

from .models import Document, Citation, Message, User
from .serializers import MessageSerializer
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

@api_view(['POST'])
def query(request):
    if request.method == 'POST':
        data = request.data

        user = request.user
        question = data.get("query", "")
        msg_object = Message(sender='user', message=question, user=request.user)
        msg_object.save()

        generated_response = retrieve_and_generate(question)['answer']
        reply = generated_response.answer.replace('\\n', '  \n')
        rply_object = Message(sender='chatbot', message=reply, user=request.user)
        rply_object.save()

        if generated_response.citations:
            for citation in generated_response.citations:
                citation.quote = re.sub(r'[\n]', '', citation.quote).strip()
                citation.quote = citation.quote.replace('\\n', ' ')
                citation_source = Document.objects.get(file=citation.source)
                citation_object = Citation(
                    message=rply_object, source=citation_source, quote=citation.quote
                )
                citation_object.save()

        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)

        return Response({'messages': serializer.data}, status=status.HTTP_200_OK)

    return Response(
        {'error': 'Method Not Allowed. Only POST method is allowed.'},
        status=status.HTTP_405_METHOD_NOT_ALLOWED
    )

def documents(request):
    documents = Document.objects.all()
    return render(request, 'marinechat/documents.html', {
        'documents': documents
    })

def serve_document(request, id):
    document = get_object_or_404(Document, id=id)
    with open(document.file.path, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{document.title}.pdf"'
        return response
