# Generated by Django 3.2.9 on 2021-11-16 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alert', '0003_auto_20211111_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contributors',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contributeur', to='alert.projects'),
        ),
    ]
