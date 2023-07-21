# Generated by Django 4.2.3 on 2023-07-21 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
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
                ("status", models.SmallIntegerField(max_length=1)),
                ("external_id", models.CharField(max_length=60, unique=True)),
                ("score", models.DecimalField(decimal_places=2, max_digits=12)),
                ("preapproved_at", models.DateTimeField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Loan",
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
                ("status", models.SmallIntegerField(max_length=1)),
                ("external_id", models.CharField(max_length=60, unique=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12)),
                ("contract_version", models.CharField(blank=True, max_length=30)),
                ("maximum_payment_date", models.DateTimeField()),
                ("taken_at", models.DateTimeField(blank=True)),
                ("outstanding", models.DecimalField(decimal_places=2, max_digits=12)),
                (
                    "customer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="loanpro_api.customer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Payment",
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
                ("status", models.SmallIntegerField(max_length=1)),
                ("external_id", models.CharField(max_length=60, unique=True)),
                ("total_amount", models.DecimalField(decimal_places=10, max_digits=20)),
                ("paid_at", models.DateTimeField()),
                (
                    "customer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="loanpro_api.customer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PaymentDetail",
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
                ("amount", models.DecimalField(decimal_places=10, max_digits=20)),
                (
                    "loan_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="loanpro_api.loan",
                    ),
                ),
                (
                    "payment_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="loanpro_api.payment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]