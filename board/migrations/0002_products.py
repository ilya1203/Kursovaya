# Generated by Django 3.0.2 on 2021-03-09 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('price', models.CharField(max_length=255, verbose_name='Цена')),
                ('fromClient', models.CharField(max_length=255, verbose_name='Логин')),
            ],
        ),
    ]
