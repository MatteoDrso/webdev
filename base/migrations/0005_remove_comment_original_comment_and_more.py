# Generated by Django 4.0.5 on 2022-06-29 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_comment_original_comment_alter_comment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='original_comment',
        ),
        migrations.AddField(
            model_name='comment',
            name='original_post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='base.comment'),
        ),
    ]