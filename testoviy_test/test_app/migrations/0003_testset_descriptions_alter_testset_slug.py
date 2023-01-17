# Generated by Django 4.1.4 on 2022-12-27 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_testset_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='testset',
            name='descriptions',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='testset',
            name='slug',
            field=models.CharField(auto_created=True, default=None, editable=False, max_length=120),
        ),
    ]
