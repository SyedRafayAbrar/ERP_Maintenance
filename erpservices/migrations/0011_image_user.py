# Generated by Django 5.0.1 on 2024-01-31 09:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpservices', '0010_imagesmodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image_User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='erpservices.imagesmodel')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'image_user',
            },
        ),
    ]