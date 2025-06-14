# Generated by Django 5.2.2 on 2025-06-09 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='media',
            name='admin_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='admin_id',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='admin_id',
        ),
        migrations.RemoveField(
            model_name='news',
            name='admin_id',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='blog_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='media',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='news',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='media_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Research_articles',
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Blog',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='News',
        ),
        migrations.DeleteModel(
            name='Media',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
