from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Client, Products, Place, Contacts_name, Contacts_phone 



def add_prod(request):  
    for cl in Client.objects.all():
        if cl.login == request.session['user']:
            for pr in Products.objects.all():
                if pr.fromClient == cl and pr.name == request.GET['name']:
                    for pl in Place.objects.all():
                        if pl.place == request.GET['place']:
                            pl.count = request.GET['count']
                            pl.save()
                            return redirect('/index/')
                    place = Place.objects.create(place=request.GET['place'], count=request.GET['count'], fromProduct=pr)
                    return redirect('/index/')                   
            prod = Products.objects.create(name=request.GET['name'], price=request.GET['price'], fromClient = cl)
            place = Place.objects.create(place=request.GET['place'], count=request.GET['count'], fromProduct=prod)
    return redirect('/index/')


def logout(request):
        request.session['user'] = ''
        request.session['id'] = ''
        return redirect('login')

    
def login(request):
    try:
        if request.session['user'] != '':
            return redirect('index')
    except:
        pass
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
    try:
        if request.session['user'] == '':
            return redirect('login')
    except:
        return redirect('login')
    
    #Get user id
    id_c = 0
    for cl in Client.objects.all():
        if cl.login == request.session['user']:
            id_c= cl.pk
    #Get products
    product = Products.objects.filter(fromClient=id_c)
    
    prod_to_exp = []
    max_price = max_count =0
    is_placed = False
    last = ''
    last_price = ''
    for p in product:
        if max_price < int(p.price):
            max_price = int(p.price)
        for place in Place.objects.filter(fromProduct=p.pk):
            if max_count < int(place.count):
                max_count = int(place.count)
            if p.name != last and p.price != last_price:
                last = p.name
                last_price = p.price
                prod_to_exp.append({'name':p.name,
                                'price': p.price,
                                'uprice': p.price,
                                'place':place.place,
                                'count': place.count,
                                'uname':p.name,
                                'countPer':0})
                
                is_placed = True
            else:
                prod_to_exp.append({'name':'',
                                'price': '',
                                'uprice': p.price,
                                'place':place.place,
                                'count': place.count,
                                'uname':p.name,
                                'countPer':0})
                is_placed = True
        
        if not is_placed:
                prod_to_exp.append({'name':p.name,
                                'price': p.price,
                                'place':'',
                                'uprice': p.price,
                                'count':'',
                                'uname':f'NP{p.name}NP',
                                'countPer':0})
    prods_graph = []

    for p in range(len(prod_to_exp)):
        prod_to_exp[p]['countPer'] = int(100*int(prod_to_exp[p]['count'])/max_count)
    for p in product:
        prods_graph.append({
            'name':p.name,
            'width': int((int(p.price)/max_price)*100)
            })
        print(int(int(p.price)/max_price)*100)
    response = render(request, 'pages/index.html', {'User': request.session['user'], 'prods':prod_to_exp, 'prods_graph':prods_graph})
    
    return response

def remove_prod(request, name, price, place, count):
    FLAG = False
    for cli in Client.objects.all():
        if cli.login == request.session['user']:
            for sname in Products.objects.filter(fromClient=cli.pk):
                if sname.name == name and sname.price == price:
                    for pl in Place.objects.filter(fromProduct=sname.pk):
                        if pl.place == place and pl.count == count:
                            pl.delete()
                            FLAG = True
                    else:
                        if FLAG:
                            if len(Place.objects.filter(fromProduct=sname.pk)) == 0:
                                sname.delete()
                            return redirect('index')
    
    return redirect('index')

def contacts(request):
    nums = Contacts_name.objects.filter(client=request.session['id'])
    cont = []
    last = ''
    for n in nums:
        for num in Contacts_phone.objects.filter(name=n.pk):
            if last != n.name:
                cont.append({'name': n.name, 'phone': num.phone, 'uname':n.name})
                last = n.name
            else:
                cont.append({'name': '', 'phone': num.phone,    'uname':n.name})
                
    
    response = render(request, 'pages/contacts.html', {'User': request.session['user'], 'cont':cont})
    
    return response

def add_contact(request):
    try:
        clients, phones_name, phones = Client.objects.all(), Contacts_name.objects.all(), Contacts_phone.objects.all()
        for cli in clients:
            if cli.login == request.session['user']:
                for name in Contacts_name.objects.filter(client=cli.pk):
                    if name.name == request.GET['name']:
                        for phone in Contacts_phone.objects.filter(name=name.pk):
                            if phone.phone == request.GET['num']:
                                return reditrect('contacts')
                        Contacts_phone.objects.create(name=name, phone=request.GET['num'])
                        return redirect('contacts')
                cont = Contacts_name.objects.create(name=request.GET['name'], client=cli)
                Contacts_phone.objects.create(name=cont, phone=request.GET['num'])

    except Exception as ex:
        print(f'Error from add contact: {ex}')

    return redirect('contacts')

def remove_contact(request, name, phone):
    try:
        clients, phones_name, phones = Client.objects.all(), Contacts_name.objects.all(), Contacts_phone.objects.all()
        for cli in clients:
            if cli.login == request.session['user']:
                for sname in Contacts_name.objects.filter(client=cli.pk):
                    print(sname.name, name,sep='-')
                    if sname.name == name:
                        for iphone in Contacts_phone.objects.filter(name=sname.pk):
                            if iphone.phone == phone:
                                iphone.delete()
                                return redirect('contacts')
    except Exception as ex:
        print(f'Err: {ex}')
        return redirect('login')
    return redirect('contacts')

def about(request):
    response = render(request, 'pages/about.html', {'User': request.session['user']})
    return response
