# Generated by Django 3.1 on 2020-08-10 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bildungsspre_chApplikation', '0007_auto_20200810_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='related_fields',
        ),
        migrations.AddField(
            model_name='field',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='_field_related_+', to='Bildungsspre_chApplikation.Field'),
        ),
    ]