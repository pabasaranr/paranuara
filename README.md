# Hello Earth! Welcome to Paranuara API

## To deploy please follow the following steps. 
I assume that you have installed Python3.7 and MySQL already. 

### Install pip
- UBUNTU : `sudo apt install python-pip`
- WINDOWS : Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py) to a folder on your computer.
    - Open a command prompt window and navigate to the folder containing **get-pip.py**. 
    - Then run 
    - `python get-pip.py `
    - This will install pip.
#### To make sure **pip** is installed
- `pip -V`

### Navigate to the desired project location
- UBUNTU : `cd path/to/folder`
- WINDOWS : `cd path\to\folder`

### Install Virtual Environment
- `pip install virtualenv`

### Create a virtual environment 
- UBUNTU : `virtualenv -p /usr/bin/python3 env_name`
- WINDOWS : `virtualenv env_name`
#### Wait until creation is complete

### Git Clone
- `git clone https://github.com/pabasaranr/paranuara.git`

### Activate the virtual environment
- UBUNTU : `source env_name/bin/activate`
- WINDOWS : `env_name\Scripts\activate`
#### When it is activated you will see a change in promt as `(env_name)...$`
#### For your information, to *deactivate* just type `deactivate`. But don't do it yet.

### Install the dependancies
#### First navigate to paranuara
- `cd paranuara`
#### Then,
- `pip install -r requirements.txt`
#### Wait until all the dependancies are installed

### Create a new schema for Paranuara (MySQL)
- ``CREATE SCHEMA `paranuara` ;`` 

### Change paranuara/settings.py
#### Open paranuara/settings.py through an editor
#### As of now we have 
``DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'paranuara',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        },
        'HOST': 'localhost',
        'USER': '',  # username
        'PASSWORD': '',  # password
    }
}``
#### Change **USER** and **PASSWORD** field using your local instance user and password (in MySQL)
#### After the changes it should look something like
``DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'paranuara',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        },
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '123',
    }
}``

### Apply migrations 
- `python manage.py makemigrations rest_api`
- `python manage.py migrate`

### To run unit tests
- `python manage.py test`
#### Make sure there are no Failures and Errors. (I hope not. :))

### Run!
- `python manage.py runserver`

# Possible improvements : 
As for the given json, most of users have themself as their friends. I didn't consider that. I can be my own friend ;).
Add an authentication.


