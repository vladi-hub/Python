# Generated by Django 2.0.3 on 2018-03-27 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homeinventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='location',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='homeinventory.Location'),
            preserve_default=False,
        ),
    ]
