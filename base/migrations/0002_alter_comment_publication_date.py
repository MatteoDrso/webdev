# Generated by Django 4.0.5 on 2022-06-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='publication_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]