# Generated by Django 5.1.2 on 2024-11-18 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sellerApp", "0011_alter_user_alternate_mobile_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="alternate_mobile_number",
            field=models.CharField(default=1, max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=25),
        ),
    ]
