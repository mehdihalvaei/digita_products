# Generated by Django 4.2.17 on 2025-01-05 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='category',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='updated time'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_time',
            field=models.DateTimeField(auto_now=True, verbose_name='update time time'),
        ),
    ]
