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




### dotenv
```
https://pypi.org/project/django-dotenv/
https://github.com/jpadilla/django-dotenv




#!/usr/bin/env python
import os
import sys

import dotenv


if __name__ == "__main__":
    dotenv.read_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


    
```




# email sending in django
```
https://docs.djangoproject.com/en/5.2/topics/email/

from django.core.mail import EmailMessage

email = EmailMessage(
    "Hello",
    "Body goes here",
    "from@example.com",
    ["to1@example.com", "to2@example.com"],
    ["bcc@example.com"],
    reply_to=["another@example.com"],
    headers={"Message-ID": "foo"},
)

```