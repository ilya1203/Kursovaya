from django.contrib import admin

from .models import Client, Products, Place, Contacts_name, Contacts_phone


admin.site.register(Place)
admin.site.register(Client)
admin.site.register(Products)
admin.site.register(Contacts_phone)
admin.site.register(Contacts_name)
# Register your models here.
