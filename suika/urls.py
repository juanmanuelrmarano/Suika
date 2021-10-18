"""suika URL Configuration

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
from suika.views import index
from suika.views import product
from suika.views import ingreso
from suika.views import registro
from suika.views import login
from suika.views import logout

urlpatterns = [
    path('',index),
    path('index/<int:page>',index),

    path('product/id=<str:idproduct>/',product),

    path('logreg/',ingreso),
    path('logreg/regExitoso=<str:regExitoso>/diffPass=<str:diffPass>',ingreso),
    path('logreg/loginState=<str:loginState>',ingreso),
    path('logreg/publicHash=<str:publicHash>/loginState=<str:loginState>',ingreso),

    path('registro/',registro),

    path('login/',login),

    path('logout/',logout),
]
