# Generated by Django 3.2.5 on 2021-08-04 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0008_rename_name_category_c_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='c_name',
            new_name='name',
        ),
    ]