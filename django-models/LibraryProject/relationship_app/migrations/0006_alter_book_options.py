# Generated by Django 5.1.4 on 2025-01-15 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0005_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('can_add_book', 'add-book'), ('can_change_book', 'change-book'), ('can_delete_book', 'delete-book')]},
        ),
    ]
