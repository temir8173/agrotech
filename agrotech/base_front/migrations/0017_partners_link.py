# Generated by Django 4.2.1 on 2023-07-08 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_front', '0016_partners'),
    ]

    operations = [
        migrations.AddField(
            model_name='partners',
            name='link',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
