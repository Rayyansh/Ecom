# Generated by Django 5.1.2 on 2024-11-16 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sellerApp", "0002_alter_termsandconditions_date_signed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productuploadmethod",
            name="preferred_shipping_method",
            field=models.CharField(
                choices=[
                    ("Self-Managed Shipping", "Self-Managed Shipping"),
                    ("World2Door Shipping Services", "World2Door Shipping Services"),
                ],
                max_length=200,
            ),
        ),
        migrations.AlterField(
            model_name="productuploadmethod",
            name="upload_method",
            field=models.CharField(
                choices=[
                    ("Manual Product Upload", "Manual Product Upload"),
                    (
                        "Bulk Product Upload (CSV/Excel)",
                        "Bulk Product Upload (CSV/Excel)",
                    ),
                    (
                        "Sync with Existing Website/CRM",
                        "Sync with Existing Website/CRM",
                    ),
                ],
                max_length=200,
            ),
        ),
    ]
