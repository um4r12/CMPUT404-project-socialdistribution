# Generated by Django 2.1.5 on 2020-03-05 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20200305_0533'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_file',
            field=models.FileField(default='media/petal.png', upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='published',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
