# Generated by Django 3.1 on 2020-08-10 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bildungsspre_chApplikation', '0005_auto_20200810_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='description',
            name='field',
            field=models.ForeignKey(default='Wissenschaftlich', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='fields', to='Bildungsspre_chApplikation.field'),
        ),
        migrations.AlterField(
            model_name='description',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='Bildungsspre_chApplikation.word'),
        ),
        migrations.AlterField(
            model_name='field',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='_field_related_+', to='Bildungsspre_chApplikation.Field'),
        ),
        migrations.AlterField(
            model_name='word',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='_word_related_+', to='Bildungsspre_chApplikation.Word'),
        ),
    ]