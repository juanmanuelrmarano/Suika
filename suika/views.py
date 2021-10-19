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
    searchTerm = request.GET.get('search')
    if searchTerm:
        data = requests.get('https://suikaapi.herokuapp.com/search?search={}'.format(request.GET.get('search')))
        search = True
    else:
        data = requests.get('https://suikaapi.herokuapp.com/contenidos?pageNum={}'.format(page))
        search = False

    data = data.json()
    
    #print(data)

    #print(request.COOKIES.get('publicHash'), request.COOKIES.get('loggedIn'))

    pageCant = data['total']//9
    print(pageCant, data['total'])

    if page == pageCant:
        nextPage = 0
    else:
        nextPage = page + 1
    
    if page == 0:
        previousPage = 0
    else:
        previousPage = page - 1

    doc = loader.get_template("index.html")

    ctx = {
        'pageCant': pageCant,
        'nextPage': nextPage,
        'previousPage': previousPage,
        'page' : page,
        'data' : data,
        'search': search,
        'loggedin': request.COOKIES.get('loggedIn')
    }

    #print(ctx)

    doc = doc.render(ctx) 

    return HttpResponse(doc)

def product(request, idproduct):
    doc = loader.get_template("product.html")

    # data = requests.get('http://127.0.0.1:5000/product?Id={}'.format(idproduct))
    data = requests.get('https://suikaapi.herokuapp.com/product?Id={}'.format(idproduct))    
    data = data.json()

    ctx = {
        'PageId': data['results'][0]['PageId'],
        'Id': data['results'][0]['Id'],
        'Title': data['results'][0]['Title'],
        'Link'  : data['results'][0]['Link'], 
        'Image': data['results'][0]['Image'],
        'Price': data['results'][0]['Price'],
        # 'History': requests.get('http://127.0.0.1:5000/history?Id={}'.format(idproduct)).json(),
        'History': requests.get('https://suikaapi.herokuapp.com/history?Id={}'.format(idproduct)).json(),
        'loggedin': request.COOKIES.get('loggedIn')
    }

    # print(ctx)

    doc = doc.render(ctx)

    return HttpResponse(doc)

# def history(request, idproduct):
#     doc = loader.get_template("product.html")

#     data = requests.get('http://127.0.0.1:5000/history?Id={}'.format(idproduct))
#     data = data.json()

#     ctx = {
#         'PageId': data['results'][0]['PageId'],
#         'Id': data['results'][0]['Id'],
#         'Price': data['results'][0]['Price'],
#         'Date': data['results'][0]['Date'],
#         'loggedin': request.COOKIES.get('loggedIn')
#     }

#     doc = doc.render(ctx)

#     return HttpResponse(doc)


def ingreso(request, regExitoso = None, diffPass = None, loginState = None, publicHash = None):
    doc = loader.get_template("loginreg.html")

    print(request.COOKIES.get('publicHash'), request.COOKIES.get('loggedIn'))

    print(regExitoso, diffPass, loginState, request.COOKIES.get('loggedIn'))

    if loginState == 'verification':
        regData = {
            'publicHash': publicHash
        }
        data = requests.put('https://suikaapi.herokuapp.com/verification', json=regData)

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
        data = requests.put('https://suikaapi.herokuapp.com/userReg', json=regData)

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
        data = requests.post('https://suikaapi.herokuapp.com/login', json=loginData)

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

