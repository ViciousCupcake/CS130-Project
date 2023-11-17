# Generated by Django 4.2.7 on 2023-11-17 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedExcelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(upload_to='excel_files/')),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
