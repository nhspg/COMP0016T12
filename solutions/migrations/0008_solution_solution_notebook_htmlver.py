# Generated by Django 2.1.5 on 2019-03-18 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0007_auto_20190307_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='solution_notebook_htmlver',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
