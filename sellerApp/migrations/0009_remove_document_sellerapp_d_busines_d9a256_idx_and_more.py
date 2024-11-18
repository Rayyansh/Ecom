# Generated by Django 5.1.2 on 2024-11-17 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "sellerApp",
            "0008_remove_document_authorized_signatory_id_thumbnail_and_more",
        ),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="document",
            name="sellerApp_d_busines_d9a256_idx",
        ),
        migrations.RemoveIndex(
            model_name="document",
            name="sellerApp_d_tax_ide_e15c9e_idx",
        ),
        migrations.RemoveIndex(
            model_name="document",
            name="sellerApp_d_proof_o_e0131e_idx",
        ),
        migrations.RemoveIndex(
            model_name="document",
            name="sellerApp_d_authori_fa2321_idx",
        ),
        migrations.AddField(
            model_name="document",
            name="authorized_signatory_id_preview",
            field=models.ImageField(blank=True, null=True, upload_to="media/previews/"),
        ),
        migrations.AddField(
            model_name="document",
            name="business_registration_document_preview",
            field=models.ImageField(blank=True, null=True, upload_to="media/previews/"),
        ),
        migrations.AddField(
            model_name="document",
            name="proof_of_business_address_preview",
            field=models.ImageField(blank=True, null=True, upload_to="media/previews/"),
        ),
        migrations.AddField(
            model_name="document",
            name="tax_identification_document_preview",
            field=models.ImageField(blank=True, null=True, upload_to="media/previews/"),
        ),
    ]
