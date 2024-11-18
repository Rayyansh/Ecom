from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import send_mail


class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'username', 'email', 'phone_number', 'is_seller', 'is_buyer', 'is_staff'
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'alternate_mobile_number')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser', 'is_seller', 'is_buyer')
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name',
                       'phone_number', 'alternate_mobile_number', 'is_seller', 'is_buyer')
        }),
    )

    search_fields = ('email', 'username')

    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)


# Rejection or approval mail body is here
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'rejection_note')
    fields = ('user',

              'business_registration_document', 'business_registration_document_expiry_date',
              'tax_identification_document', 'tax_identification_document_expiry_date',
              'proof_of_business_address', 'proof_of_business_address_expiry_date',
              'authorized_signatory_id', 'authorized_signatory_id_expiry_date',

              'is_approved', 'rejection_note')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # If the document is approved
        if obj.is_approved:
            self.send_approval_email(obj.user.email)
        else:
            rejection_note = form.cleaned_data.get('rejection_note', '')
            obj.rejection_note = rejection_note
            obj.save()
            self.send_rejection_email(obj.user.email, rejection_note)

    def send_approval_email(self, recipient_email):
        subject = 'Documents Approved'
        message = 'Your documents have been approved. You can now proceed for add products.'
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)

    def send_rejection_email(self, recipient_email, rejection_note):
        subject = 'Documents Rejected'
        message = (f'Your documents have been rejected for the following reason: {rejection_note}. Please correct and '
                   f're-submit.')
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)


admin.site.register(Document, DocumentAdmin)

admin.site.register(Seller)
admin.site.register(TeamMember)
admin.site.register(ProductUploadMethod)
admin.site.register(TermsAndConditions)
admin.site.register(SellerBank)
