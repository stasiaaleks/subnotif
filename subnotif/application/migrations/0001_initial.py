# Generated by Django 5.1.2 on 2024-12-01 19:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=256)),
                ('payment_day', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_link', models.URLField(blank=True, null=True)),
                ('is_paid', models.BooleanField(blank=True, null=True)),
            ],
        ),
    ]
