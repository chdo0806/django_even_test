# Generated by Django 4.0.2 on 2022-03-09 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('pubdate', models.DateTimeField()),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maker', to=settings.AUTH_USER_MODEL)),
                ('voter', models.ManyToManyField(blank=True, related_name='voter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chname', models.CharField(default='', max_length=200)),
                ('chpic', models.ImageField(upload_to='vote/%y/%m')),
                ('chcom', models.TextField()),
                ('choicer', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vote.topic')),
            ],
        ),
    ]