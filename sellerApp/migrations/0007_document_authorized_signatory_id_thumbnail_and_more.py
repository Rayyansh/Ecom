# Generated by Django 5.1.2 on 2024-11-17 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sellerApp", "0006_alter_document_authorized_signatory_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="authorized_signatory_id_thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/thumbnails/"
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="business_registration_document_thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/thumbnails/"
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="proof_of_business_address_thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/thumbnails/"
            ),
        ),
        migrations.AddField(
            model_name="document",
            name="tax_identification_document_thumbnail",
            field=models.ImageField(
                blank=True, null=True, upload_to="media/thumbnails/"
            ),
        ),
    ]
