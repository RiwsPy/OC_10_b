# Generated by Django 3.2.5 on 2021-08-15 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0013_auto_20210813_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite_product',
            name='product',
            field=models.CharField(max_length=100),
        ),
    ]
