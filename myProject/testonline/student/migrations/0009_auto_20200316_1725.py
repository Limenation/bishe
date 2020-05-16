# Generated by Django 2.0.6 on 2020-03-16 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_auto_20200316_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='level',
            field=models.CharField(choices=[('3', 'difficult'), ('1', 'easy'), ('2', 'general')], max_length=10, verbose_name='等级'),
        ),
        migrations.AlterField(
            model_name='student',
            name='dept',
            field=models.CharField(choices=[('信息学院', '信息学院'), ('中药学院', '中药学院'), ('护理学院', '护理学院'), ('针灸推拿康复学院', '针灸推拿康复学院')], default=None, max_length=20, verbose_name='学院'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='dept',
            field=models.CharField(choices=[('信息学院', '信息学院'), ('中药学院', '中药学院'), ('护理学院', '护理学院'), ('针灸推拿康复学院', '针灸推拿康复学院')], default=None, max_length=20, verbose_name='学院'),
        ),
    ]