# Generated by Django 4.0.2 on 2023-05-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("depot", "0002_migration"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storedfilter",
            name="id",
            field=models.AutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
