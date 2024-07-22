from django.contrib import admin
from .models import User, Document, Message

# Register your models here.
admin.site.register(User)
admin.site.register(Document)
admin.site.register(Message)
