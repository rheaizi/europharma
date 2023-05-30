from audioop import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from pharmapp.models import User, Medicine, Admins, Image


# from pharmapp.models import AdminPharm


def index(request):
    med = Medicine.objects.all()

    return render(request, 'pharmapp/index.html', {'title': 'Главная страница', 'medicines': med, 'temp': 0})


def admingoi(request):
    if request.method == "POST":
        phone = request.POST.get('phone', '0')
        password = request.POST.get('password', '0')
        existance = User.objects.filter(phone=phone, password=password).exists()

        if existance:
            # name = User.objects.get(phone=phone, password=password).name
            context = {
                'title': 'Главная страница',
                'medicines': Medicine.objects.all()
            }
            return render(request, 'pharmapp/adminlist.html', context=context)
    return render(request, 'pharmapp/adminlist.html', {'title': 'AdminPanel', 'medicines': Medicine.objects.all()})


def adminsignin(request):
    if request.method == "POST":
        phone = request.POST['phone']
        password = request.POST['password']
        existance = User.objects.filter(phone=phone, password=password).exists()

        if existance:
            context = {
                'title': 'Главная страница',
                'medicines': Medicine.objects.all()
            }
            return render(request, 'pharmapp/admingoi.html', context=context)
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, 'pharmapp/adminsignin.html')


def adminsignup(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']
        if name == "" or phone == "" or password == "":
            context = {
                'name': name,
                'phone': phone,
                'message_all': "Сначала заполните поля"
            }
            return render(request, 'pharmapp/adminsignup.html', context=context)
        if User.objects.filter(name=name):
            context = {
                'phone': phone,
                'message_name': "This name is already exist! Please try some other!"
            }
            return render(request, 'pharmapp/adminsignup.html', context=context)
        if User.objects.filter(phone=phone):
            context = {
                'name': name,
                'message_phone': "This phone is already exist! Please try some other!"
            }
            return render(request, 'pharmapp/adminsignup.html', context=context)
        if not any(isinstance(ord(char), int) for char in phone):
            # 48 > ord(char) > 57 for char in password
            context = {
                'name': name,
                'message_phone': "This phone number isn't digit!",
                'charac': phone
            }
            return render(request, 'pharmapp/adminsignup.html', context=context)
        if len(password) < 8:
            context = {
                'name': name,
                'phone': phone,
                'message': "Your password less than 8 characters"
            }
            return render(request, 'pharmapp/adminsignup.html', context=context)
        if not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(
                char.islower() for char in password):
            context = {
                'name': name,
                'phone': phone,
                'message': "Password should have at least one numeral, one uppercase letter and one lowercase letter"
            }
            return render(request, 'pharmapp/adminsignup.html', context=context)

        Admins.objects.create(name=name, phone=phone, password=password)

        return redirect('/admingoi/')
    return render(request, 'pharmapp/adminsignup.html')


def adminupdate(request, medicine_id):
    return render(request, 'pharmapp/adminupdate.html', {'medicines': Medicine.objects.get(id=medicine_id)})


def updatedb(request, medicine_id):
    med = Medicine.objects.get(id=medicine_id)
    name = request.POST.get('name', '0')
    med.name = name
    description = request.POST.get('description', '0')
    med.description = description
    price = request.POST.get('price', '0')
    med.price = price
    quantity = request.POST.get('quantity', '0')
    med.quantity = quantity
    med.save()
    return redirect('/admingoi/admin/med/')


def insertdb(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        quantity = request.POST['quantity']
        image = request.FILES['img']
        Medicine.objects.create(name=name, description=description, price=price, quantity=quantity, image=image)
        return redirect('/admingoi/admin/med/')
    return render(request, 'pharmapp/addmedicine.html', {'title': 'Добавить лекарство'})


def deleteitem(request, medicine_id):
    med = Medicine.objects.get(id=medicine_id)
    med.delete()
    return redirect('/admingoi/admin/med/')


def signin(request):
    if request.method == "POST":
        phone = request.POST.get('phone', '0')
        password = request.POST.get('password', '0')
        existance = User.objects.filter(phone=phone, password=password).exists()

        if existance:
            name = User.objects.get(phone=phone, password=password).name
            request.session['id'] = User.objects.filter(phone=phone, password=password).first().id
            context = {
                'title': 'Главная страница',
                'temp': 1,
                'name': name,
                'medicines': Medicine.objects.all()
            }
            return render(request, 'pharmapp/index.html', context=context)
        else:
            messages.error(request, "Неверный логин или пароль")

    return render(request, 'pharmapp/login.html', {'title': 'Войти в кабинет'})


def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        password = request.POST['password']
        password2 = request.POST['password2']
        if name == "" or phone == "" or password == "":
            context = {
                'name': name,
                'phone': phone,
                'message_all': "Сначала заполните поля"
            }
            return render(request, 'pharmapp/signup.html', context=context)
        if User.objects.filter(name=name):
            context = {
                'phone': phone,
                'message_name': "This name is already exist! Please try some other!"
            }
            return render(request, 'pharmapp/signup.html', context=context)
        if User.objects.filter(phone=phone):
            context = {
                'name': name,
                'message_phone': "This phone is already exist! Please try some other!"
            }
            return render(request, 'pharmapp/signup.html', context=context)
        if password != password2:
            context = {
                'name': name,
                'message': "Your password are not same in second password",
            }
            return render(request, 'pharmapp/signup.html', context=context)
        if not any(isinstance(ord(char), int) for char in phone):
            # 48 > ord(char) > 57 for char in password
            context = {
                'name': name,
                'message_phone': "This phone number isn't digit!",
                'charac': phone
            }
            return render(request, 'pharmapp/signup.html', context=context)
        if len(password) < 8:
            context = {
                'name': name,
                'phone': phone,
                'message': "Your password less than 8 characters"
            }
            return render(request, 'pharmapp/signup.html', context=context)
        if not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(
                char.islower() for char in password):
            context = {
                'name': name,
                'phone': phone,
                'message': "Password should have at least one numeral, one uppercase letter and one lowercase letter"
            }
            return render(request, 'pharmapp/signup.html', context=context)
        User.objects.create(name=name, phone=phone, password=password)
        return redirect('/signin/')

    return render(request, 'pharmapp/signup.html', {'title': 'Зарегистрироваться'})


def images(request):
    if request.method == 'POST':
        i = request.FILES['img']
        a = Image(image=i)
        a.save()
    return render(request, 'pharmapp/image.html')


def profile(request):
    context = {
        'name': User.objects.all().filter(id=request.session['id']).first().name,
        'phone': User.objects.all().filter(id=request.session['id']).first().phone,
        'password': User.objects.all().filter(id=request.session['id']).first().password,
        'id': User.objects.all().filter(id=request.session['id']).first().id,
    }
    return render(request, 'pharmapp/usercabinet.html', context)


def useredit(request, pk_id):
    context = {
        'name': User.objects.all().filter(id=request.session['id']).first().name,
        'phone': User.objects.all().filter(id=request.session['id']).first().phone,
        'password': User.objects.all().filter(id=request.session['id']).first().password,
        'id': User.objects.all().filter(id=request.session['id']).first().id,
    }
    # user = User.objects.get(id=pk_id)
    return render(request, 'pharmapp/useredit.html', context)


def userupdate(request, pk_id):
    user = User.objects.get(id=pk_id)
    user.name = request.POST.get('name', '0')
    user.phone = request.POST.get('phone', '0')
    user.password = request.POST.get('password', '0')
    user.save()
    return redirect('/profile/')


def signout(request):
    del request.session['id']
    return redirect('/signin/')


def medicine(request):
    context = {
        'medicines': Medicine.objects.all()
    }
    return render(request, 'pharmapp/admingoi.html', context)


def users(request):
    userlar = User.objects.all()
    return render(request, 'pharmapp/users.html', {'users': userlar})


def deleteusers(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('/admingoi/admin/users/')


def editusers(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        name = request.POST.get('name', '0')
        user.name = name
        phone = request.POST.get('phone', '0')
        user.phone = phone
        password = request.POST.get('password', '0')
        user.password = password
        user.save()
    user = User.objects.get(id=user_id)
    context = {
        'name': user.name,
        'phone': user.phone,
        'password': user.password,
    }
    return render(request, 'pharmapp/editusers.html', context)


def itempage(request, item_id):
    item = Medicine.objects.get(id=item_id)
    recently_viewed_items = None
    if 'recently_viewed' in request.session:
        if item_id in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(item_id)

        recently_viewed_items = Medicine.objects.filter(id__in=request.session['recently_viewed'])
        request.session['recently_viewed'].insert(0, item_id)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    else:
        request.session['recently_viewed'] = [item_id]

    request.session.modified = True
    context = {
        'item': item,
        'recently_viewed_items': recently_viewed_items
    }
    return render(request, 'pharmapp/item_page.html', context)

