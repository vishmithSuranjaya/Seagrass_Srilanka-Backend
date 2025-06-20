# Generated by Django 5.2.2 on 2025-06-09 07:57

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_actions', '0001_initial'),
        ('media', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(max_length=200)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_actions.admin')),
                ('media_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media.media')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('payment_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('count', models.IntegerField(default=1)),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
