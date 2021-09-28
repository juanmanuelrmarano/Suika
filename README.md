# Suika♥

## Developers

* Juan Manuel Rodriguez Marano

* Maribel Pereyra


## Dependencias

* python3
* django
* pymongo


## Requerimientos principales

*Es necesario instalar Mongodb. 

	Link de descarga: https://www.mongodb.com/try/download/community
	Documentación: https://docs.mongodb.com/manual/installation/

*En ambas secciones es necesario que se cree un environment. Para esto utilizando pip, podemos instalar virtualenv, que es la libreria para crear el environment.

	Para crear el entorno virtual, ejecutamos el siguiente comando:
	'python -m venv env'

    comando de activacion del environment:
    '{nombre del environment}\Scripts\activate'
    Si nuestro environment se llama 'env', el comando seria: `env\Scripts\activate`    

**Es necesario activar el environment antes de ejecutar cualquier archivo cada vez que se utilice**

*Luego de tener el environment activado, es necesario instalar los requerimientos la primera vez y cada vez que se agregue una librería al proyecto 

    El comando para instalar las librerias es:
    'pip install -r requirements.txt'


## Ejecucion de django

* Activar environment
* Abrir terminal posicionado en la ubicacion de manage.py
* Utilizar comando `python manage.py runserver` para que el servidor comience a funcionar.
* Si el servidor comienza sin problemas deberia mostrar el siguiente texto:
  
  ```
  System check identified no issues (0 silenced).
  June 25, 2020 - 23:09:24
  Django version 3.0.7, using settings 'animefountain.settings'
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.

  ```
* Utilizar la siguiente direccion para entrar a la primera pagina de la aplicacion `http://127.0.0.1:8000/index/0`

## Ejecucion del API

* Activar environment
* Abrir terminal posicionado en la ubicacion de api.py
* Utilizar comando `python api.py` para iniciar.
* Si el servidor comienza sin problemas deberia mostrar el siguiente texto:

  ```
 * Serving Flask app "api" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on https://suikaapi.herokuapp.com/// (Press CTRL+C to quit)
  ```

  Ejemplo de un llamado al API con respuesta correcta en la consola:
  127.0.0.1 - - [01/Dec/2020 23:17:56] GET /contenidos?pageNum=0 HTTP/1.10 200 -
  siendo el url del endpoint 'https://suikaapi.herokuapp.com///contenidos?pageNum=0'

## Ejecucion del Scraping

* Para guardar la data de todas las páginas es necesario:
* Activar environment
* Abrir terminal posicionado en la carpeta de scrapings
* Correr cada script con el comando 'python nombredelarchivo.py'

Los resultados se guardaran en la base de datos de Suika.
