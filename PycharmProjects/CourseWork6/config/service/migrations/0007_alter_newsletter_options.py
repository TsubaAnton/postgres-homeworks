# Generated by Django 4.2 on 2024-05-16 19:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_alter_newsletter_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'permissions': [('view_all_newsletters', 'Can view all newsletters'), ('deactivate_newsletter', 'Can deactivate newsletters')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
