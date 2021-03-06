# Generated by Django 3.2.9 on 2021-11-09 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('alert', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='author_user',
            field=models.ManyToManyField(related_name='contributions', through='alert.Contributors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issues',
            name='assignee_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assignment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issues',
            name='author_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='author_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='issues',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='alert.projects'),
        ),
        migrations.AddField(
            model_name='contributors',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='alert.projects'),
        ),
        migrations.AddField(
            model_name='contributors',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='author_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alert.issues'),
        ),
    ]
