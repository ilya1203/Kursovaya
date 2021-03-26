from django.contrib import admin

from .models import Client, Products, Contacts_name, Contacts_phone

admin.site.register(Client)
admin.site.register(Products)
admin.site.register(Contacts_phone)
admin.site.register(Contacts_name)
