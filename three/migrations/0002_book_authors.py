# Generated by Django 2.0.6 on 2020-06-30 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('three', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(db_constraint=False, related_name='books', to='three.Author'),
        ),
    ]
