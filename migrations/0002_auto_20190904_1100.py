# Generated by Django 2.2.4 on 2019-09-04 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='complementary',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='img_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='occupied_color',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='picture',
            name='opposite',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
