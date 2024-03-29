# Generated by Django 5.0.1 on 2024-02-15 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erpservices', '0016_rename_user_userinformation_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appartment_Residence_Status',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('appartment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='erpservices.appartment_info')),
                ('residence_status', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='erpservices.residence_status')),
            ],
            options={
                'db_table': 'appartment_residence_status',
            },
        ),
    ]
