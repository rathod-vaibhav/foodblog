from django.shortcuts import render

from .models import *
from django.http import HttpResponse
from django.db import connections
from django.shortcuts import redirect
from django.db.models import Count


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


def demo(request):
    with connections['user'].cursor() as cursor:
        print("0----", cursor)
        cursor.execute("SELECT * FROM user_client")
        row = cursor.fetchone()
        print("row",row)

    return render(request, "user/demo.html", {'data': row})

def order(request):
    return render(request, "user/order.html")

def orders(request):
    orderdata = Orders_Download.objects.all()
    order_places_count = Orders_Download.objects.filter(place_order=True).count()
    return render(request, "user/orders.html", {'data': orderdata, 'cdata': len(orderdata), 'oplaces': order_places_count})

def add_order(request):
    print("---", request.POST)
    name = request.POST["name"]
    lastorder = Orders_Download.objects.count() + 1
    order_num = "ORDER-"+ str(lastorder)
    Orders_Download.objects.create(person_name=name, order_num=order_num)
    
    response = redirect('/user/orders/')
    return response

def place_order(request,pk):
    print("order")
    Orders_Download.objects.filter(id=pk).update(place_order=True)
    
    response = redirect('/user/orders/')
    return response

def order_report(request):
    with connections['user'].cursor() as cursor:
        cursor.execute('SELECT created_on , count(*) FROM "order" group by created_on')
        row_data = cursor.fetchall()
        print("row_data",row_data)

    place_order_data = Orders_Download.objects.extra({'date_created' : "date(datetime_created)"}).values('updated_on').annotate(created_count=Count('id'))
    print("place_order_data", place_order_data)
    place_or_data = {}
    for place_data in place_order_data:
        place_or_data[place_data["updated_on"].strftime('%Y-%m-%d')] = place_data["created_count"]
    print(":place_or_data",place_or_data)
    data = []
    
    for row in row_data:
        responce = {}
        responce["date"] = row[0].strftime('%Y-%m-%d')
        responce["download_order"] = row[1]
        responce["place_order"] = place_or_data[row[0].strftime('%Y-%m-%d')] if row[0].strftime('%Y-%m-%d') in place_or_data else 0
        data.append(responce)
    print("data", data)
    return render(request, "user/order_report.html", {'data': data})
