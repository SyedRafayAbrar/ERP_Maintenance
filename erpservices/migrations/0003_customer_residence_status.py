# Generated by Django 5.0.1 on 2024-01-20 17:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpservices', '0002_residence_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_Residence_Status',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('residence_status', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='erpservices.residence_status')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'customer_residence_status',
            },
        ),
    ]
