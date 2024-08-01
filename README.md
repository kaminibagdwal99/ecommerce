# ecommerce


>>add in templates in setting.py



>>in project folder inside grearkart /greatkart whree setting.py also rerside
 crete a static folder and in setting.py
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR /'static'
STATICFILES_DIRS = ['greatkart/static',]


run : python manage.py collectstatic it will create a static folder with admin folder inside in greatkart folder

change the path with {% load static %}

AUTH_USER_MODEL = 'accounts.Account'

# vitual

py -m venv env
env\Scripts\activate

