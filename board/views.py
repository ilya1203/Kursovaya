from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Client,Products, Contacts_name, Contacts_phone

def index(request):
    if request.GET:
        print(request.GET)
        msg = ''
        clients = Client.objects.all()
        FLAG = True
        product = []
        if 'nameProd' in request.GET :
            try:
                if request.GET['nameProd'] != '':
                    try:
                        price=str(int(request.GET['priceProd']))
                        Products.objects.create(name=request.GET['nameProd'],
                                            price=price, fromClient=request.GET['login'])
                    except:
                        pass
                    return redirect(f"/index/?login={request.GET['login']}&password={request.GET['password']}")
            except:
                return redirect(f"/index/?login={request.GET['login']}&password={request.GET['password']}")
        else:
            f_price = 0
            for client in clients:
                if client.login == request.GET['login'] and client.psw == request.GET['password']:
                    FLAG = False
                    for p in Products.objects.all():
                        if p.fromClient == request.GET['login']:
                            product.append(p)
                            f_price += int(p.price)
                    contacts = []
                    tm_ar = []
                    counter = 1
                    for c in Contacts_name.objects.all():
                        if str(c.client) == str(request.GET['login']):
                            contacts.append({'name':c, 'nums': Contacts_phone.objects.filter(name=str(c.pk))})
                    else:
                        print(contacts)
                    return render(request, 'home.html', {'name':request.GET['login'],
                                                         'psw':request.GET['password'], 'prod': product, 'total':f_price, 'contacts':contacts})  
                if client.login == request.GET['login']:
                    msg = 'Неправильный пароль'
                    return render(request, 'index.html', {'er':msg})  
            if FLAG:
                if request.GET['login'] != '' and request.GET['password'] != '':
                    Client.objects.create(login=request.GET['login'] , psw = request.GET['password'] )
                    return render(request, 'home.html', {'name':request.GET['login']})
                else:
                    msg = 'Некоректоный логин или пароль'
                    return render(request, 'index.html', {'er':msg}) 
    else:
        return render(request, 'index.html', {})

def config(request, config):
    if config == 'exit':
        return redirect(f"/index/")
