# Generated by Django 2.1.7 on 2019-04-16 16:30

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0009_auto_20190319_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solution',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AlterField(
            model_name='solution',
            name='solution_notebook',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
