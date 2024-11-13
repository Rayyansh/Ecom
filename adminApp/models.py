from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    Gender = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=Gender)
    address = models.TextField()
    phone_number = models.CharField(max_length=25)
    country = CountryField()
    profile_photo = models.ImageField(upload_to='profile_photos/')

    class Meta:
        indexes = [
            models.Index(fields=['is_seller']),
            models.Index(fields=['is_buyer']),
            models.Index(fields=['gender']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['country']),
            models.Index(fields=['profile_photo']),
        ]

    def __str__(self):
        return self.username


class Seller(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    business_name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=100)
    business_type = models.CharField(max_length=255)
    tax_identification_number = models.CharField(max_length=100)

    bank_name = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=100)
    bank_ifsc_code = models.CharField(max_length=11)
    bank_branch = models.CharField(max_length=255)

    # Permission s for share info with buyer

    share_business_name = models.BooleanField(default=False)
    share_address = models.BooleanField(default=False)
    share_gender = models.BooleanField(default=False)
    share_phone_number = models.BooleanField(default=False)
    share_country = models.BooleanField(default=False)
    share_registration_number = models.BooleanField(default=False)
    share_business_type = models.BooleanField(default=False)
    share_tax_identification_number = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['business_name']),
            models.Index(fields=['registration_number']),
            models.Index(fields=['business_type']),
            models.Index(fields=['tax_identification_number']),
            models.Index(fields=['bank_name']),
            models.Index(fields=['bank_account_number']),
            models.Index(fields=['bank_ifsc_code']),
            models.Index(fields=['bank_branch']),
        ]

    def __str__(self):
        return self.business_name


class Document(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')

    aadhar_card = models.FileField(upload_to='documents/')
    aadhar_card_expiry_date = models.DateField(help_text="Expiry date of the Aadhaar card")

    pan_card = models.FileField(upload_to='documents/')
    pan_card_expiry_date = models.DateField(help_text="Expiry date of the Pan card")

    gst_licence = models.FileField(upload_to='documents/')
    gst_licence_expiry_date = models.DateField(help_text="Expiry date of the G.S.T. Licence")

    shop_act = models.FileField(upload_to='documents/')
    shop_act_expiry_date = models.DateField(help_text="Expiry date of the Shop Act")

    trade_licence = models.FileField(upload_to='documents/')
    trade_licence_expiry_date = models.DateField(help_text="Expiry date of the Trade Licence")

    is_approved = models.BooleanField(default=False)
    rejection_note = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['aadhar_card', 'aadhar_card_expiry_date']),
            models.Index(fields=['pan_card', 'pan_card_expiry_date']),
            models.Index(fields=['gst_licence', 'gst_licence_expiry_date']),
            models.Index(fields=['shop_act', 'shop_act_expiry_date']),
            models.Index(fields=['trade_licence', 'trade_licence_expiry_date']),
        ]

    def __str__(self):
        return f"Documents for {self.user.username}"
