# Generated by Django 2.2.3 on 2019-07-28 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorderapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='custisactive',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], db_column='custIsActive', max_length=1),
        ),
        migrations.AlterField(
            model_name='person',
            name='personactive',
            field=models.CharField(choices=[('yes', 'yes'), ('nno', 'no')], db_column='personActive', max_length=1),
        ),
    ]