from django.shortcuts import render

from .models import *


# Create your views here.
def index(request):
    # Index Page
    return render(request, "user/index.html")


def registration_page(request):
    # Registration Page
    return render(request, "user/registration.html")


def login_page(request):
    # Login Page
    if 'email' in request.session:
        udi = Client.objects.get(email=request.session['email'])
        print('<-------login udi------->',udi)
        return render(request, "user/index.html", {'udi': udi})
    else:
        return render(request, "user/login.html")


def registration(request):
    # Registration Data Collect
    if 'email' in request.session:
        udi = Client.objects.get(email=request.session['email'])
        return render(request, "user/index.html", {'udi': udi})
    else:

        u_email = request.POST['email']
        u_name = request.POST['username']
        u_password = request.POST['password']
        u_gender = request.POST['gender']
        u_phonenumber = request.POST['phonenumber']

        uid = Client.objects.create(email=u_email, username=u_name, password=u_password, gender=u_gender,
                                    phonenumber=u_phonenumber)

        if uid:
            print("<--------------Registration Successfully!!-------------->")
            smsg = 'Registration Successfully!!'
            return render(request, "user/login.html", {'smsg': smsg})
        else:
            print('<--------------Registraton Error..!!-------------->')
            emsg = 'Registration Incomplate!'
            return render(request, "user/registration.html", {'emsg': emsg})


def login_evalute(request):
    # login logic
    try:
        u_email = request.POST['email']
        u_password = request.POST['password']

        uid = Client.objects.get(email=u_email)
        print("<------------->", uid)
        if uid:
            if uid.password == u_password:
                request.session['username'] = uid.username
                request.session['email'] = uid.email
                return render(request, "user/index.html", {'uid': uid})
            else:
                emsg = 'Password is incrrect!!'
                return render(request, "user/login.html", {'emsg': emsg})
        else:
            emsg = 'Email Or Password Invalid!!!!!'
            return render(request, "user/login.html", {'emsg': emsg})
    except:
        emsg = 'Email Or Password Invalid!!'
        return render(request, "user/login.html", {'emsg': emsg})


def logout(request):
    #if logout by user as direct index page open
    if 'email' in request.session:
        del request.session['username']
        del request.session['email']
        return render(request, "user/login.html")
    else:
        return render(request, "user/login.html")


# client data view , delete, edit
def view_all(request):
    data = Client.objects.all()
    cdata = Client.objects.all().count()
    return render(request, "user/view_all.html", {'data': data, 'cdata': cdata})


def delete_data(request, pk):
    uid = Client.objects.get(id=pk)
    uid.delete()
    data = Client.objects.all()
    cdata = Client.objects.all().count()
    return render(request, "user/view_all.html", {'data': data, 'cdata': cdata})


def edit_data(request, pk):
    uid = Client.objects.get(id=pk)
    return render(request, "user/edit_data.html", {'udi': uid})


def update(request):
    id = request.POST['id']
    email = request.POST['email']
    username = request.POST['username']
    password = request.POST['password']
    phonenumber = request.POST['phonenumber']

    uid = Client.objects.get(id=id)

    uid.email = email
    uid.username = username
    uid.password = password
    uid.phonenumber = phonenumber

    uid.save()

    data = Client.objects.all()
    cdata = Client.objects.all().count()
    return render(request, "user/view_all.html", {'data': data, 'cdata': cdata})
