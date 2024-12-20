# Generated by Django 5.1.2 on 2024-11-16 09:00

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                ("is_seller", models.BooleanField(default=True)),
                ("is_buyer", models.BooleanField(default=False)),
                ("email", models.EmailField(max_length=254)),
                ("phone_number", models.CharField(max_length=25)),
                ("alternate_mobile_number", models.CharField(max_length=25)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Document",
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
                (
                    "business_registration_document",
                    models.FileField(upload_to="documents/"),
                ),
                (
                    "business_registration_document_expiry_date",
                    models.DateField(
                        help_text="Expiry date of the Business Registration Document"
                    ),
                ),
                (
                    "tax_identification_document",
                    models.FileField(upload_to="documents/"),
                ),
                (
                    "tax_identification_document_expiry_date",
                    models.DateField(
                        help_text="Expiry date of the Tax Identification Document"
                    ),
                ),
                ("proof_of_business_address", models.FileField(upload_to="documents/")),
                (
                    "proof_of_business_address_expiry_date",
                    models.DateField(
                        help_text="Expiry date of the Proof of Business Address"
                    ),
                ),
                ("authorized_signatory_id", models.FileField(upload_to="documents/")),
                (
                    "authorized_signatory_id_expiry_date",
                    models.DateField(
                        help_text="Expiry date of the Authorized Signatory ID"
                    ),
                ),
                ("is_approved", models.BooleanField(default=False)),
                ("rejection_note", models.TextField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Seller",
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
                ("business_name", models.CharField(max_length=255)),
                (
                    "business_type",
                    models.CharField(
                        choices=[
                            (
                                "Sole Establishment/Sole Proprietorship",
                                "Sole Establishment/Sole Proprietorship",
                            ),
                            ("Civil Company", "Civil Company"),
                            (
                                "Limited Liability Company (LLC)",
                                "Limited Liability Company (LLC)",
                            ),
                            ("Free Zone Company", "Free Zone Company"),
                            (
                                "Free Zone Establishment (FZE)",
                                "Free Zone Establishment (FZE)",
                            ),
                            (
                                "Free Zone Company (FZC) or Free Zone LLC (FZ LLC)",
                                "Free Zone Company (FZC) or Free Zone LLC (FZ LLC)",
                            ),
                            (
                                "Branch Office of a Foreign Company",
                                "Branch Office of a Foreign Company",
                            ),
                            ("Representative Office", "Representative Office"),
                            (
                                "Public Joint Stock Company (PJSC)",
                                "Public Joint Stock Company (PJSC)",
                            ),
                            (
                                "Private Joint Stock Company (PrJSC)",
                                "Private Joint Stock Company (PrJSC)",
                            ),
                            ("Offshore Company", "Offshore Company"),
                        ],
                        max_length=255,
                    ),
                ),
                ("business_registration_number", models.CharField(max_length=100)),
                (
                    "date_of_business_establishment",
                    models.DateField(blank=True, null=True),
                ),
                ("address_line_1", models.CharField(max_length=255)),
                ("address_line_2", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("seller_country", django_countries.fields.CountryField(max_length=2)),
                ("postal_code", models.IntegerField()),
                ("website_url", models.URLField(blank=True, null=True)),
                (
                    "business_category",
                    models.CharField(
                        choices=[
                            ("Fashion & Accessories", "Fashion & Accessories"),
                            ("Electronics", "Electronics"),
                            ("Home & Kitchen", "Home & Kitchen"),
                            ("Health & Beauty", "Health & Beauty"),
                            ("Sports & Outdoors", "Sports & Outdoors"),
                            ("Toys & Games", "Toys & Games"),
                            ("Arts & Crafts", "Arts & Crafts"),
                            ("Books & Media", "Books & Media"),
                            ("Other (Specify)", "Other (Specify)"),
                        ],
                        max_length=100,
                    ),
                ),
                ("brand_information", models.TextField(blank=True, null=True)),
                ("share_business_name", models.BooleanField(default=False)),
                ("share_registration_number", models.BooleanField(default=False)),
                ("share_business_type", models.BooleanField(default=False)),
                ("share_tax_identification_number", models.BooleanField(default=False)),
                ("share_phone_number", models.BooleanField(default=False)),
                ("share_alternate_phone_number", models.BooleanField(default=False)),
                ("share_email", models.BooleanField(default=False)),
                ("share_address_line_1", models.BooleanField(default=False)),
                ("share_address_line_2", models.BooleanField(default=False)),
                ("share_city", models.BooleanField(default=False)),
                ("share_state", models.BooleanField(default=False)),
                ("share_seller_country", models.BooleanField(default=False)),
                ("share_postal_code", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductUploadMethod",
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
                (
                    "upload_method",
                    models.CharField(
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
                        max_length=50,
                    ),
                ),
                (
                    "platform_type",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "api_keys",
                    models.TextField(
                        blank=True,
                        help_text="Provide API keys if applicable",
                        null=True,
                    ),
                ),
                (
                    "technical_contact_name",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "technical_contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "technical_contact_phone",
                    models.CharField(blank=True, max_length=25, null=True),
                ),
                (
                    "preferred_shipping_method",
                    models.CharField(
                        choices=[
                            ("Self-Managed Shipping", "Self-Managed Shipping"),
                            (
                                "World2Door Shipping Services",
                                "World2Door Shipping Services",
                            ),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "seller",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_upload_method",
                        to="sellerApp.seller",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SellerBank",
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
                ("bank_name", models.CharField(max_length=255)),
                ("bank_account_number", models.CharField(max_length=100)),
                ("swift_bic_code", models.CharField(max_length=20)),
                ("account_holder_name", models.CharField(max_length=100)),
                (
                    "bank_address",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "seller",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="seller_bank",
                        to="sellerApp.seller",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TeamMember",
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
                (
                    "full_name_1",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "teammate_email_1",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "teammate_role_1",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Product Manager", "Product Manager"),
                            ("Order Fulfillment", "Order Fulfillment"),
                            ("Finance", "Finance"),
                            ("Admin", "Admin"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "full_name_2",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "teammate_email_2",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "teammate_role_2",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Product Manager", "Product Manager"),
                            ("Order Fulfillment", "Order Fulfillment"),
                            ("Finance", "Finance"),
                            ("Admin", "Admin"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "full_name_3",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "teammate_email_3",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "teammate_role_3",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Product Manager", "Product Manager"),
                            ("Order Fulfillment", "Order Fulfillment"),
                            ("Finance", "Finance"),
                            ("Admin", "Admin"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "full_name_4",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "teammate_email_4",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "teammate_role_4",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Product Manager", "Product Manager"),
                            ("Order Fulfillment", "Order Fulfillment"),
                            ("Finance", "Finance"),
                            ("Admin", "Admin"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "full_name_5",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "teammate_email_5",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "teammate_role_5",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Product Manager", "Product Manager"),
                            ("Order Fulfillment", "Order Fulfillment"),
                            ("Finance", "Finance"),
                            ("Admin", "Admin"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
                ("is_active_1", models.BooleanField(default=True)),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="team_members",
                        to="sellerApp.seller",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TermsAndConditions",
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
                (
                    "agreement",
                    models.BooleanField(
                        default=False,
                        help_text="Compliance with local and international e-commerce regulations.\nAdhering to fair trade practices and product listing policies.\nFollowing World2Door’s return and refund policies for customer orders.\nEnsuring all information provided is accurate and up-to-date.\nPlease check this box to confirm that you agree to these terms.",
                    ),
                ),
                ("signature", models.BooleanField(default=False)),
                ("date_signed", models.DateField(auto_now_add=True)),
                (
                    "seller",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="terms_and_conditions",
                        to="sellerApp.seller",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="user",
            index=models.Index(
                fields=["email", "phone_number", "alternate_mobile_number"],
                name="sellerApp_u_email_bf81d7_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=[
                    "business_registration_document",
                    "business_registration_document_expiry_date",
                ],
                name="sellerApp_d_busines_d9a256_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=["tax_identification_document", "tax_identification_document"],
                name="sellerApp_d_tax_ide_e15c9e_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=[
                    "proof_of_business_address",
                    "proof_of_business_address_expiry_date",
                ],
                name="sellerApp_d_proof_o_e0131e_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="document",
            index=models.Index(
                fields=[
                    "authorized_signatory_id",
                    "authorized_signatory_id_expiry_date",
                ],
                name="sellerApp_d_authori_fa2321_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="seller",
            index=models.Index(
                fields=["address_line_1", "address_line_2"],
                name="sellerApp_s_address_2ba0c3_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="seller",
            index=models.Index(
                fields=["city", "state", "seller_country", "postal_code"],
                name="sellerApp_s_city_30e6bf_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="seller",
            index=models.Index(
                fields=[
                    "business_name",
                    "business_type",
                    "business_registration_number",
                    "date_of_business_establishment",
                ],
                name="sellerApp_s_busines_1663ba_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="seller",
            index=models.Index(
                fields=["website_url", "business_category", "brand_information"],
                name="sellerApp_s_website_da720a_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="productuploadmethod",
            index=models.Index(
                fields=["upload_method"], name="sellerApp_p_upload__46a339_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="productuploadmethod",
            index=models.Index(
                fields=["platform_type", "api_keys"],
                name="sellerApp_p_platfor_9aa69c_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="productuploadmethod",
            index=models.Index(
                fields=[
                    "technical_contact_name",
                    "technical_contact_email",
                    "technical_contact_phone",
                ],
                name="sellerApp_p_technic_462014_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="productuploadmethod",
            index=models.Index(
                fields=["preferred_shipping_method"],
                name="sellerApp_p_preferr_627a28_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sellerbank",
            index=models.Index(
                fields=["bank_name", "bank_account_number"],
                name="sellerApp_s_bank_na_ffe86d_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sellerbank",
            index=models.Index(
                fields=["swift_bic_code", "account_holder_name"],
                name="sellerApp_s_swift_b_2ce181_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="sellerbank",
            index=models.Index(
                fields=["bank_address"], name="sellerApp_s_bank_ad_a08900_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="teammember",
            index=models.Index(
                fields=["full_name_1", "teammate_email_1", "teammate_role_1"],
                name="sellerApp_t_full_na_82a6f5_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="teammember",
            index=models.Index(
                fields=["full_name_2", "teammate_email_2", "teammate_role_2"],
                name="sellerApp_t_full_na_32cc11_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="teammember",
            index=models.Index(
                fields=["full_name_3", "teammate_email_3", "teammate_role_3"],
                name="sellerApp_t_full_na_46e7b9_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="teammember",
            index=models.Index(
                fields=["full_name_4", "teammate_email_4", "teammate_role_4"],
                name="sellerApp_t_full_na_64232d_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="teammember",
            index=models.Index(
                fields=["full_name_5", "teammate_email_5", "teammate_role_5"],
                name="sellerApp_t_full_na_0bbfbd_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="termsandconditions",
            index=models.Index(
                fields=["agreement"], name="sellerApp_t_agreeme_9f8b44_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="termsandconditions",
            index=models.Index(
                fields=["signature"], name="sellerApp_t_signatu_11af62_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="termsandconditions",
            index=models.Index(
                fields=["date_signed"], name="sellerApp_t_date_si_ec11a6_idx"
            ),
        ),
    ]
