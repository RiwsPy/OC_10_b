# Generated by Django 3.2.5 on 2021-08-04 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_auto_20210804_1630'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name',
            new_name='c_name',
        ),
    ]
