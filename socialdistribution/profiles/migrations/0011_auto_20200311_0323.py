# Generated by Django 2.1.5 on 2020-03-11 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20200310_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_img',
            field=models.ImageField(default='temp.jpg', upload_to='profile/'),
        ),
    ]