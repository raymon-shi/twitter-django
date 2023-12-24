# Generated by Django 5.0 on 2023-12-24 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashtag', models.CharField(max_length=50)),
                ('tweet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tweet.tweet')),
            ],
        ),
    ]
