# Generated by Django 3.1.4 on 2021-03-29 14:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20210316_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dummy',
            name='first_img',
        ),
        migrations.RemoveField(
            model_name='dummy',
            name='second_img',
        ),
        migrations.RemoveField(
            model_name='dummy',
            name='third_img',
        ),
    ]