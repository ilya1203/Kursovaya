# Generated by Django 3.0.2 on 2021-06-09 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fullstack', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'ordering': ['login']},
        ),
        migrations.AlterField(
            model_name='place',
            name='fromProduct',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.PROTECT, to='fullstack.Products', verbose_name='Имя продукта'),
            preserve_default=False,
        ),
    ]