# Generated by Django 4.2.7 on 2023-11-08 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fuski_Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the fuseki relationship.', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Description of the fuseki relationship.')),
                ('attribute1', models.CharField(help_text='First attribute in the relationship.', max_length=255)),
                ('attribute2', models.CharField(help_text='Second attribute in the relationship.', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Fuski_Relations_Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the group of relationships.', max_length=255)),
                ('description', models.TextField(blank=True, help_text='Description of the group of relationships.')),
                ('relations', models.ManyToManyField(help_text='Relationships between attributes.', to='app.fuski_relation')),
            ],
        ),
    ]
