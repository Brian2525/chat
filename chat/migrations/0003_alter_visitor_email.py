# Generated by Django 5.1.1 on 2024-10-22 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_thread_visitor_delete_chatmessage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]