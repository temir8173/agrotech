# Generated by Django 4.2.1 on 2023-07-11 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_front', '0019_alter_partners_link_alter_partners_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=255)),
                ('locale', models.CharField(choices=[('kk', 'Kazakh'), ('ru', 'Russian'), ('en', 'English')], default='kk', max_length=4)),
                ('logo', models.ImageField(upload_to='consulting_logo/')),
                ('description', models.TextField(blank=True, max_length=1500, null=True)),
            ],
        ),
    ]
