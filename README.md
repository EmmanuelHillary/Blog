# Blog
A little blog with CRUD functionalities and authentication system

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/EmmanuelHillary/Blog.git
$ cd Blog
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ py -3 -m venv env
$ env\Scripts\activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment 

Once `pip` has finished downloading the dependencies:

```sh
(env)$ cd project
```
make make migrations and push the migrations

```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate

```

create an admin user

```sh
(env)$ python manage.py createsuperuser
```

then run the server

```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.

**Homepagae**
![Alt text](https://github.com/EmmanuelHillary/Blog/blob/main/images/posts.png "Homepage")

**Register Page**
![Alt text](https://github.com/EmmanuelHillary/Blog/blob/main/images/register.png "register")

**Login Page**
![Alt text](https://github.com/EmmanuelHillary/Blog/blob/main/images/login.png "login")

**Edit profile Page**
![Alt text](https://github.com/EmmanuelHillary/Blog/blob/main/images/Edit%20profile.png "profile")

**Post Detail Page**
![Alt text](https://github.com/EmmanuelHillary/Blog/blob/main/images/detail%20page.png "post detail")

**Post Comments**
![Alt text](https://github.com/EmmanuelHillary/Blog/blob/main/images/comments.png "comments")





