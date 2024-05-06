# Generated by Django 4.2.11 on 2024-05-04 10:34

import common.methods
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("vendors", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PurchaseOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "po_number",
                    models.CharField(
                        default=common.methods.get_unique_code_chars,
                        editable=False,
                        max_length=16,
                        unique=True,
                    ),
                ),
                ("order_date", models.DateTimeField()),
                ("delivery_date", models.DateTimeField()),
                ("items", models.JSONField()),
                ("quantity", models.IntegerField()),
                ("issue_date", models.DateTimeField(blank=True, null=True)),
                ("acknowledgment_date", models.DateTimeField(blank=True, null=True)),
                ("quality_rating", models.FloatField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("PENDING", "pending"),
                            ("COMPLETED", "completed"),
                            ("CANCELLED", "cancelled"),
                        ],
                        default="PENDING",
                        max_length=50,
                    ),
                ),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="purchase_orders",
                        to="vendors.vendor",
                    ),
                ),
            ],
            options={
                "verbose_name": "Purchase Order",
                "verbose_name_plural": "Purchase Orders",
                "ordering": ["-order_date"],
            },
        ),
    ]