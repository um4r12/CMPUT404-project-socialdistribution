# Generated by Django 2.1.5 on 2020-03-05 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20200305_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='published',
            field=models.DateTimeField(auto_now_add=True, editable=False, verbose_name='date published'),
        ),
    ]
