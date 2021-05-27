from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Client, Products, Place, Contacts_name, Contacts_phone 

def comment()   :
    for prod in Products.objects.all():
        if prod.name == request.GET['name']:
            prod.price = request.GET['price']
            prod.save()
            for place in Place.objects.all():
                if place.fromProduct == prod.name and place.place == request.GET['place']:
                    place.count = request.GET['count']
                    place.save()
                    return redirect('index')
            else:
                place = Place()
                place.fromProcuct = prod.pk
                place.place = request.GET['place']
                place.count = request.GET['count']
                place.save()
                return redirect('index')

def add_prod(request):  
    for cl in Client.objects.all():
        if cl.login == request.session['user']:
            prod = Products.objects.create(name=request.GET['name'], price=request.GET['price'], fromClient = cl)
            for prod in Products.objects.filter(fromClient=cl.pk):
                if prod.name == request.GET['name']:
                    place = Place()
                    place.fromProcuct = prod
                    place.place = request.GET['place']
                    place.count = request.GET['count']
                    place.save()
                    print(cl, prod, place)
                
    return redirect('/index/')


def logout(request):
        request.session['user'] = ''
        request.session['id'] = ''
        return redirect('login')

def login(request):
    if request.session['user'] != '':
        return redirect('index')
    if request.GET:
        FLAG = True
        if request.GET != dict():
            for c in Client.objects.all():
                if request.GET['login'] == c.login:
                    FLAG = False
                    if request.GET['password'] == c.psw:
                        request.session['user'] = request.GET['login']
                        request.session['id'] = c.pk
                        print(request.session['user'])
                        return redirect('index')
                    else:
                        return render(request,'login/login.html', {'er': 'У данного пользователя другой пароль)'})
            if FLAG:
                        cli = Client()
                        cli.login = request.GET['login']
                        cli.psw = request.GET['password']
                        cli.save()
                        request.session['user'] = cli.login
                        request.session['id'] = cli.pk
                        return redirect('login')
    
    return render(request,'login/login.html', {'er': ''})

def index(request):
    if request.session['user'] == '':
        return redirect('login')
    
    #Get user id
    id_c = 0
    for cl in Client.objects.all():
        if cl.login == request.session['user']:
            id_c= cl.pk
    
    #Get products
    product = Products.objects.filter(fromClient=id_c)
    
    prod_to_exp = []
    prod_to_exp.append({'name':'Название',
                                'price': 'Цена',
                                'place':'Место',
                                'count': 'Количество'})
    is_placed = False
    for p in product:
        for place in Place.objects.filter(fromProduct=p.pk):
            if p.name != prod_to_exp[-1]['name']:
                prod_to_exp.append({'name':p.name,
                                'price': p.price,
                                'place':place.place,
                                'count': place.count})
                is_placed = True
            else:
                prod_to_exp.append({'name':'',
                                'price': '',
                                'place':place.place,
                                'count': place.count})
                is_placed = True
        
        if not is_placed:
                print(p.name)
                prod_to_exp.append({'name':p.name,
                                'price': p.price,
                                'place':'',
                                'count':''})
    response = render(request, 'pages/index.html', {'User': request.session['user'], 'prods':prod_to_exp})
    
    return response

def contacts(request):
    
    nums = Contacts_name.objects.filter(client=request.session['id'])
    cont = [{'name':'', 'phone':''}]
    print(nums)
    for n in nums:
        for num in Contacts_phone.objects.filter(name=n.pk):
            if cont[-1]['name'] != n.name:
                cont.append({'name': n.name, 'phone': num.phone})
            else:
                cont.append({'name': '', 'phone': num.phone})
    
    response = render(request, 'pages/contacts.html', {'User': request.session['user'], 'cont':cont})
    
    return response

def add_contact(request):
    try:
        pass
    except:
        pass

    return redirect('contacts')

def about(request):
    response = render(request, 'pages/about.html', {'User': request.session['user']})
    return response
