# Generated by Django 3.0.4 on 2020-03-10 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0003_auto_20200310_0605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meters',
            name='fuel',
            field=models.CharField(choices=[(None, '(Unknown)'), (1, 'Water'), (2, 'Natural Gas'), (3, 'Electricity')], max_length=20),
        ),
    ]
