from django.contrib import admin

# Register your models here.
from .models import GroupMessage, Category, Configuration, Message

admin.site.register(GroupMessage)
admin.site.register(Category)
admin.site.register(Configuration)
admin.site.register(Message)
