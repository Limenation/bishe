# Generated by Django 2.0.6 on 2020-03-16 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20200316_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('1', 'easy'), ('2', 'general'), ('3', 'difficult')], max_length=10, verbose_name='等级'),
        ),
    ]
