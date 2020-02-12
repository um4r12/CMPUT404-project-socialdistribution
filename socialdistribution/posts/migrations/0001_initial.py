# Generated by Django 2.1.5 on 2020-02-08 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostId',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('post_author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.AuthorId')),
            ],
        ),
    ]