# Generated by Django 5.0 on 2024-01-31 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articleApp', '0005_remove_article_texteintegral'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='texteIntegral',
            field=models.TextField(blank=True, default=''),
        ),
    ]
