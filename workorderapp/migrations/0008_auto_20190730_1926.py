# Generated by Django 2.2.3 on 2019-07-30 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workorderapp', '0007_updates_refdomainid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='updates',
            options={'verbose_name': 'Work Order Updates'},
        ),
        migrations.AlterModelOptions(
            name='workorder',
            options={'ordering': ('-woid',), 'verbose_name': 'Work Order'},
        ),
    ]
