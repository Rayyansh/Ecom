# Generated by Django 5.1.2 on 2024-11-18 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sellerApp", "0012_alter_user_alternate_mobile_number_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="seller",
            name="business_category",
            field=models.CharField(
                choices=[
                    ("Fashion & Accessories", "Fashion & Accessories"),
                    ("Electronics", "Electronics"),
                    ("Home & Kitchen", "Home & Kitchen"),
                    ("Health & Beauty", "Health & Beauty"),
                    ("Sports & Outdoors", "Sports & Outdoors"),
                    ("Toys & Games", "Toys & Games"),
                    ("Arts & Crafts", "Arts & Crafts"),
                    ("Books & Media", "Books & Media"),
                ],
                max_length=100,
            ),
        ),
    ]
