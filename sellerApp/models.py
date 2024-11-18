from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from pdf2image import convert_from_path
from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
import os
from phonenumber_field.modelfields import PhoneNumberField



class User(AbstractUser):
    is_seller = models.BooleanField(default=True)
    is_buyer = models.BooleanField(default=False)

    email = models.EmailField()
    phone_number = models.CharField(max_length=25)
    alternate_mobile_number = models.CharField(max_length=25)

    class Meta:
        indexes = [
            models.Index(fields=['email', 'phone_number', 'alternate_mobile_number']),
        ]

    def __str__(self):
        return self.username


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('Product Manager', 'Product Manager'),
        ('Order Fulfillment', 'Order Fulfillment'),
        ('Finance', 'Finance'),
        ('Admin', 'Admin')
    ]

    seller = models.ForeignKey('Seller', on_delete=models.CASCADE, related_name='team_members')

    full_name_1 = models.CharField(max_length=100, blank=True, null=True)
    teammate_email_1 = models.EmailField(blank=True, null=True)
    teammate_role_1 = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    full_name_2 = models.CharField(max_length=100, blank=True, null=True)
    teammate_email_2 = models.EmailField(blank=True, null=True)
    teammate_role_2 = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    full_name_3 = models.CharField(max_length=100, blank=True, null=True)
    teammate_email_3 = models.EmailField(blank=True, null=True)
    teammate_role_3 = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    full_name_4 = models.CharField(max_length=100, blank=True, null=True)
    teammate_email_4 = models.EmailField(blank=True, null=True)
    teammate_role_4 = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    full_name_5 = models.CharField(max_length=100, blank=True, null=True)
    teammate_email_5 = models.EmailField(blank=True, null=True)
    teammate_role_5 = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True, null=True)

    is_active_1 = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['full_name_1', 'teammate_email_1', 'teammate_role_1']),
            models.Index(fields=['full_name_2', 'teammate_email_2', 'teammate_role_2']),
            models.Index(fields=['full_name_3', 'teammate_email_3', 'teammate_role_3']),
            models.Index(fields=['full_name_4', 'teammate_email_4', 'teammate_role_4']),
            models.Index(fields=['full_name_5', 'teammate_email_5', 'teammate_role_5']),
        ]

    def __str__(self):
        return f"{self.seller}"


class Seller(models.Model):
    BUSINESS_TYPE = [
        ('Sole Establishment/Sole Proprietorship', 'Sole Establishment/Sole Proprietorship'),
        ('Civil Company', 'Civil Company'),
        ('Limited Liability Company (LLC)', 'Limited Liability Company (LLC)'),
        ('Free Zone Company', 'Free Zone Company'),
        ('Free Zone Establishment (FZE)', 'Free Zone Establishment (FZE)'),
        ('Free Zone Company (FZC) or Free Zone LLC (FZ LLC)', 'Free Zone Company (FZC) or Free Zone LLC (FZ LLC)'),
        ('Branch Office of a Foreign Company', 'Branch Office of a Foreign Company'),
        ('Representative Office', 'Representative Office'),
        ('Public Joint Stock Company (PJSC)', 'Public Joint Stock Company (PJSC)'),
        ('Private Joint Stock Company (PrJSC)', 'Private Joint Stock Company (PrJSC)'),
        ('Offshore Company', 'Offshore Company'),
    ]

    BUSINESS_CATEGORY = [
        ('Fashion & Accessories', 'Fashion & Accessories'),
        ('Electronics', 'Electronics'),
        ('Home & Kitchen', 'Home & Kitchen'),
        ('Health & Beauty', 'Health & Beauty'),
        ('Sports & Outdoors', 'Sports & Outdoors'),
        ('Toys & Games', 'Toys & Games'),
        ('Arts & Crafts', 'Arts & Crafts'),
        ('Books & Media', 'Books & Media'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=255, choices=BUSINESS_TYPE)
    business_registration_number = models.CharField(max_length=100)
    date_of_business_establishment = models.DateField(blank=True, null=True)

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255)

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    seller_country = CountryField()
    postal_code = models.IntegerField()

    website_url = models.URLField(blank=True, null=True)
    business_category = models.CharField(max_length=100, choices=BUSINESS_CATEGORY)
    brand_information = models.TextField(blank=True, null=True)

    # Permissions for share info with buyer

    share_business_name = models.BooleanField(default=False)
    share_registration_number = models.BooleanField(default=False)
    share_business_type = models.BooleanField(default=False)

    share_address_line_1 = models.BooleanField(default=False)
    share_address_line_2 = models.BooleanField(default=False)

    share_city = models.BooleanField(default=False)
    share_state = models.BooleanField(default=False)
    share_seller_country = models.BooleanField(default=False)
    share_postal_code = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['address_line_1', 'address_line_2']),
            models.Index(fields=['city', 'state', 'seller_country', 'postal_code']),
            models.Index(fields=['business_name', 'business_type', 'business_registration_number',
                                 'date_of_business_establishment']),
            models.Index(fields=['website_url', 'business_category', 'brand_information']),
        ]

    def __str__(self):
        return self.business_name


class Document(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')

    business_registration_document = models.FileField(upload_to='media/documents/')
    business_registration_document_expiry_date = models.DateField(
        help_text="Expiry date of the Business Registration Document")

    tax_identification_document = models.FileField(upload_to='media/documents/')
    tax_identification_document_expiry_date = models.DateField(
        help_text="Expiry date of the Tax Identification Document")

    proof_of_business_address = models.FileField(upload_to='media/documents/')
    proof_of_business_address_expiry_date = models.DateField(help_text="Expiry date of the Proof of Business Address")

    authorized_signatory_id = models.FileField(upload_to='media/documents/')
    authorized_signatory_id_expiry_date = models.DateField(help_text="Expiry date of the Authorized Signatory ID")

    is_approved = models.BooleanField(default=False)
    rejection_note = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['business_registration_document', 'business_registration_document_expiry_date']),
            models.Index(fields=['tax_identification_document', 'tax_identification_document']),
            models.Index(fields=['proof_of_business_address', 'proof_of_business_address_expiry_date']),
            models.Index(fields=['authorized_signatory_id', 'authorized_signatory_id_expiry_date']),
        ]

    def __str__(self):
        return f"Documents for {User.first_name} {User.last_name}"



class ProductUploadMethod(models.Model):
    UPLOAD_CHOICES = [
        ('Manual Product Upload', 'Manual Product Upload'),
        ('Bulk Product Upload (CSV/Excel)', 'Bulk Product Upload (CSV/Excel)'),
        ('Sync with Existing Website/CRM', 'Sync with Existing Website/CRM')
    ]

    SHIPPING_CHOICES = [
        ('Self-Managed Shipping', 'Self-Managed Shipping'),
        ('World2Door Shipping Services', 'World2Door Shipping Services')
    ]

    seller = models.OneToOneField('Seller', on_delete=models.CASCADE, related_name='product_upload_method')

    upload_method = models.CharField(max_length=200, choices=UPLOAD_CHOICES)

    platform_type = models.CharField(max_length=100, blank=True, null=True)
    api_keys = models.TextField(blank=True, null=True, help_text="Provide API keys if applicable")

    technical_contact_name = models.CharField(max_length=100, blank=True, null=True)
    technical_contact_email = models.EmailField(blank=True, null=True)
    technical_contact_phone = models.CharField(max_length=25, blank=True, null=True)

    preferred_shipping_method = models.CharField(max_length=200, choices=SHIPPING_CHOICES)

    class Meta:
        indexes = [
            models.Index(fields=['upload_method']),
            models.Index(fields=['platform_type', 'api_keys']),
            models.Index(fields=['technical_contact_name', 'technical_contact_email', 'technical_contact_phone']),
            models.Index(fields=['preferred_shipping_method']),
        ]

    def __str__(self):
        return self.seller.business_name


class TermsAndConditions(models.Model):
    seller = models.OneToOneField('Seller', on_delete=models.CASCADE, related_name='terms_and_conditions')
    agreement = models.BooleanField(
        default=False,
        help_text=(
            "Compliance with local and international e-commerce regulations.\n"
            "Adhering to fair trade practices and product listing policies.\n"
            "Following World2Door’s return and refund policies for customer orders.\n"
            "Ensuring all information provided is accurate and up-to-date.\n"
            "Please check this box to confirm that you agree to these terms."
        )
    )

    signature = models.BooleanField(default=False)
    date_signed = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['agreement']),
            models.Index(fields=['signature']),
            models.Index(fields=['date_signed']),
        ]

    def __str__(self):
        return self.seller.business_name


class SellerBank(models.Model):
    seller = models.OneToOneField('Seller', on_delete=models.CASCADE, related_name='seller_bank')

    bank_name = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=100)

    swift_bic_code = models.CharField(max_length=20)
    account_holder_name = models.CharField(max_length=100)

    bank_address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['bank_name', 'bank_account_number']),
            models.Index(fields=['swift_bic_code', 'account_holder_name']),
            models.Index(fields=['bank_address']),
        ]

    def __str__(self):
        return self.seller.business_name
