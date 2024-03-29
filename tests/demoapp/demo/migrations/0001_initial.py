# Generated by Django 5.0.1 on 2024-03-05 19:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Artist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flags", models.JSONField(blank=True, default=dict, null=True)),
                ("name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("full_name", models.CharField(max_length=255)),
                ("year_of_birth", models.IntegerField()),
                ("active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Band",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "genre",
                    models.IntegerField(
                        choices=[(1, "Rock"), (2, "Blues"), (3, "Soul"), (4, "Other")]
                    ),
                ),
                ("active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Countries",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="DemoModelField",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("flags", models.JSONField(blank=True, default=dict, null=True)),
                ("char", models.CharField(max_length=255)),
                ("integer", models.IntegerField()),
                ("logic", models.BooleanField(default=False)),
                ("date", models.DateField()),
                ("datetime", models.DateTimeField()),
                ("time", models.TimeField()),
                ("decimal", models.DecimalField(decimal_places=3, max_digits=10)),
                ("email", models.EmailField(max_length=254)),
                ("float", models.FloatField()),
                ("bigint", models.BigIntegerField()),
                ("generic_ip", models.GenericIPAddressField()),
                ("url", models.URLField()),
                ("text", models.TextField()),
                ("json", models.JSONField()),
                ("unique", models.CharField(max_length=255, unique=True)),
                ("nullable", models.CharField(max_length=255, null=True)),
                ("blank", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "not_editable",
                    models.CharField(
                        blank=True, editable=False, max_length=255, null=True
                    ),
                ),
                (
                    "choices",
                    models.IntegerField(
                        choices=[(1, "Choice 1"), (2, "Choice 2"), (3, "Choice 3")]
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Artist_IntersectionFieldListFilter",
            fields=[],
            options={
                "verbose_name": "IntersectionFieldListFilter",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("demo.artist",),
        ),
        migrations.CreateModel(
            name="Artist_RelatedFieldCheckBoxFilter",
            fields=[],
            options={
                "verbose_name": "RelatedFieldCheckBoxFilter",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("demo.artist",),
        ),
        migrations.CreateModel(
            name="Artist_RelatedFieldRadioFilter",
            fields=[],
            options={
                "verbose_name": "RelatedFieldRadioFilter",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("demo.artist",),
        ),
        migrations.CreateModel(
            name="Artist_UnionFieldListFilter",
            fields=[],
            options={
                "verbose_name": "UnionFieldListFilter",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("demo.artist",),
        ),
        migrations.AddField(
            model_name="artist",
            name="bands",
            field=models.ManyToManyField(
                related_name="bands", to="demo.band", verbose_name="Bands"
            ),
        ),
        migrations.AddField(
            model_name="artist",
            name="favourite_city",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="demo.city"
            ),
        ),
        migrations.AddField(
            model_name="artist",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="demo.country"
            ),
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="demo.country"
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="city",
            name="region",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="demo.region"
            ),
        ),
    ]
