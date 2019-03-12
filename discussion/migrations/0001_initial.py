# Generated by Django 2.1.4 on 2019-03-12 14:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.TextField(default='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Developer')),
            ],
        ),
    ]
