"""foodblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('', views.index, name='index'),
    path('r-page/', views.registration_page, name='registration-page'),
    path('login-page/', views.login_page, name='login-page'),
    #logic pages (reg,login)
    path('registration/', views.registration, name='registration'),
    path('login-evalute/',views.login_evalute,name='login-evalute'),
    path('logout/',views.logout,name='logout'),
    #client data view
    path('view-all/',views.view_all,name='view-all'),
    path('delete-data/<int:pk>',views.delete_data,name='delete-data'),
    path('edit-data/<int:pk>', views.edit_data, name='edit-data'),
    path('update/',views.update,name='update'),
    path('demo/',views.demo,name='demo'),
    path('add_order/',views.add_order,name='add_order'),
    path('orders/',views.orders,name='orders'),
    path('order/',views.order,name='order'),
    path('place_order/<int:pk>',views.place_order,name='place_order'),
    path('order_report/',views.order_report,name='order_report'),

]
