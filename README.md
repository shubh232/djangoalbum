# DjangoAlbum
A Image Album with User Authentication and RESTful implementation made using Django.

**Author:** Shubh Srivastava

## Getting Started

Clone this repo to any directory.

```
https://github.com/shubh232/djangoalbum.git
```
Assuming python is in the PATH,start up a new virtual environment.

```
$ cd djangoalbum
$ python -m venv ENV
$ source ENV/bin/activate
```
If windows go to,

```
> cd ENV/Scripts
> activate
```

Once the environment is active, install all the project dependencies.There is a **requirements** file which can be used to do a pip install.

```
(ENV)$ pip install -r requirements.txt
```
Navigate to project root , to djangoalbum and apply all the database migrations.

```
(ENV)$ cd djangoalbum
(ENV)$ python manage.py makemigrations
(ENV)$ python manage.py makemigrations accounts
(ENV)$ python manage.py makemigrations albums
(ENV)$ python manage.py migrate
```
Finally , run the server to serve the app on localhost.
```
(ENV)$ python manage.py runserver
```
Django serves at port 8000, unless specified otherwise. The locally-served site can be accessed at http://localhost:8000

## Features

* User Profile for storing information about the User.
* Album attached to users having various information like Title , Cover , Photos , Publishing Privacy,Date Created etc.
* Photos for each user having various information like Title , Description , Publishing Privacy , Date Created etc.
* Public Albums and Photos
* Possible to edit and delete the Albums and Photos
* API endpoints supporting CRUD operation for Album models and Update,Delete options for User models.
* Like Button for each photo and album used by registered users.

## Models

This app allows user to store and organize albums and photos.
It contains 3 models . **User Profile** , **Album** and **Photo**.

**The `User Profile` model contains**
- First Name
- Last Name
- Email
- Password
- Bio
- Address
- Gender
- Personal Website

**The `Photo` model contains**
- Title
- Description
- Date Created
- Date Modified
- Date of Publishing
- Image File

**The `Album` model contains**
- Title
- Description
- Date Created
- Date Modified
- Date of Publishing
- Multiple Photos
- Cover Photo

## URL Routes
- `/` - Home Page
- `accounts/register/` - Register a User
- `login/` - Login a user
- `accounts/profile/` - Account of the logged in user
- `edit/` - Edit Profile of User.
- `photos/add/` - Add Photo
- `albums/add/` - Add Albums
- `albums/` - Public Album
- `photos/` - Public Photos
- `library/` - User Library
- `api/albums/`- API EndPoint for Album
- `api/users/` - API EndPoint for Users
## Build With
* [Django](https://www.djangoproject.com/) - The web framework
* [Django Rest Framework](http://www.django-rest-framework.org/) - REST framework
