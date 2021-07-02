from django.http import HttpResponse
import datetime
import pymongo
import requests
import hashlib
from django.template import Template, Context
from django.template import loader
from django.shortcuts import render
from django.shortcuts import redirect
from django.template.defaulttags import register
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def index(request, page=0):
    data = requests.get('http://127.0.0.1:5000/contenidos?pageNum={}'.format(page))
    data = data.json()

    print(data)

    print(request.COOKIES.get('publicHash'), request.COOKIES.get('loggedIn'))

    pageCant = data['total']//9

    nextPage = page + 1

    if page == 0:
        previousPage = 0
        previousPages = 0
    elif page == 1:
        previousPage = 0
        previousPages = 1
    else:
        previousPage = page - 1
        previousPages = 2

    pageNumbers = []
    pageDelimiter = 0
    for i in range(page-previousPages,pageCant):
        pageDelimiter += 1
        if pageDelimiter == 6:
            break
        pageNumbers.append(i)
        print(i)

    doc = loader.get_template("index.html")

    ctx = {
        'pageNumbers': pageNumbers,
        'pageCant': pageCant,
        'nextPage': nextPage,
        'previousPage': previousPage,
        'page' : page,
        'data' : data,
        'loggedin': request.COOKIES.get('loggedIn')
    }

    print(ctx)

    doc = doc.render(ctx) 

    return HttpResponse(doc)

def ingreso(request, regExitoso = None, diffPass = None, loginState = None, publicHash = None):
    doc = loader.get_template("loginreg.html")

    print(request.COOKIES.get('publicHash'), request.COOKIES.get('loggedIn'))

    print(regExitoso, diffPass, loginState, request.COOKIES.get('loggedIn'))

    if loginState == 'verification':
        regData = {
            'publicHash': publicHash
        }
        data = requests.put('http://127.0.0.1:5000/verification', json=regData)

    ctx = {
        'regExitoso' : regExitoso,
        'diffPass': diffPass,
        'loginState': loginState,
        'loggedin': request.COOKIES.get('loggedIn')
    }

    print(ctx)

    doc = doc.render(ctx)

    return HttpResponse(doc)

def registro(request):
    form = request.POST

    regExitoso = "True"
    diffPass = "None"
 
    if form['pass'] == form['pass2']:
        diffPass = "False"
    else:
        diffPass = "True"

    if form['email'] != '' and form['pass'] != '':
        tohash = form['email'] + form['pass']
        hashSecure = hashlib.sha256(tohash.encode('UTF-8')).hexdigest()
        publicHash = hashlib.md5(tohash.encode('UTF-8')).hexdigest()

        regData = {
            'email': form['email'],
            'hashSHA256': hashSecure,
            'publicHash': publicHash
        }
        data = requests.put('http://127.0.0.1:5000/userReg', json=regData)

        if data.json()['success'] == False:
            regExitoso = "False"
        else:
            send_mail(
                'Requerimos activacion de tu cuenta',
                f"""Gracias por registrarse en Suika!
                Por favor, activa tu cuenta siguiendo este link:
                
                http://127.0.0.1:8000/logreg/publicHash={publicHash}/loginState=verification""",
                'support@suika.com',
                [form['email']],
                fail_silently=False,
            )
        
    response = redirect(f'/logreg/regExitoso={regExitoso}/diffPass={diffPass}')

    return response

def logout(request):
    print(request.COOKIES.get('publicHash'), request.COOKIES.get('loggedIn'))
    
    response = redirect(f'/index/0')
    response.set_cookie('publicHash',None)
    response.set_cookie('loggedIn',None)

    print(request.COOKIES.get('publicHash'), request.COOKIES.get('loggedIn'))

    return response

def login(request):
    form = request.POST

    if form['email'] != '' and form['pass'] != '':
        tohash = form['email'] + form['pass']
        hashSecure = hashlib.sha256(tohash.encode('UTF-8')).hexdigest()
        publicHash = hashlib.md5(tohash.encode('UTF-8')).hexdigest()

        loginData = {
            'email': form['email'],
            'hashSHA256': hashSecure,
            'publicHash': publicHash
        }
        data = requests.post('http://127.0.0.1:5000/login', json=loginData)

        loginState = data.json()['loginState']

        if loginState == 'ok':
            response = redirect(f'/index/0')
            response.set_cookie('publicHash',publicHash)
            response.set_cookie('loggedIn',True)
        else:
            response = redirect(f'/logreg/loginState={loginState}')
            response.set_cookie('publicHash',None)
            response.set_cookie('loggedIn',None)

    return response        
