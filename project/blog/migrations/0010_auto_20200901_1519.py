# Generated by Django 3.0.7 on 2020-09-01 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20200901_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postimage',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='post images/'),
        ),
    ]