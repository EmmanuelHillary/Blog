import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Post
from faker import Faker
from django.utils import timezone
from django.utils.text import slugify
import random


def create_users(n):
    fake_data = Faker()
    for _ in range(n):
        name = fake_data.name().split()
        fname = name[0]
        lname = name[1]
        User.objects.create_user(
            username=fname,
            first_name=fname,
            last_name=lname,
            email=f'{fname+lname}@mail.com',
            password=f'{fname}password'
        )


def create_posts(n):
    fake_data = Faker()
    for _ in range(n):
        id = random.randint(1, 10)
        title = fake_data.job()
        status = random.choice(['draft', 'published'])
        Post.objects.create(
            title=title,
            slug=slugify(title),
            author=User.objects.get(id=id),
            body=fake_data.text(),
            created=timezone.now(),
            updated=timezone.now(),
            status=status
        )



print('Operation is a success!!')
