# Create Project
```
pip install django
django-admin startproject djangoauthapi
python manage.py startapp account
python manage.py makemigrations
python manage.py migrate

```

# DRD
```
https://www.django-rest-framework.org/

// command to install

```


# django jwt tokens
```
https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html


pip install djangorestframework-simplejwt

REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}


// we create token manually https://django-rest-framework-simplejwt.readthedocs.io/en/latest/creating_tokens_manually.html



from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# setting.py check and understand it.  https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
```




# django-cors-headers
```
# https://pypi.org/project/django-cors-headers/


pip install django-cors-headers
```




# make environment file .env
```
# pip install python-dotenv


```




# custom auth model for auth
```
https://docs.djangoproject.com/en/5.2/topics/auth/customizing/



https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#a-full-example



```