from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import send_mail


class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'username', 'email', 'phone_number', 'is_seller', 'is_buyer', 'is_staff', 'is_active', 'country'
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'gender', 'address', 'phone_number',
                       'country', 'is_seller', 'is_buyer')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'gender', 'address',
                       'phone_number', 'country', 'is_seller', 'is_buyer')
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)



admin.site.register(User, CustomUserAdmin)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'registration_number', 'business_type')
    search_fields = ('business_name', 'user__username')
    list_filter = ('business_type',)


# Rejection or approval mail body is here
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_approved', 'rejection_note')
    fields = ('user', 'aadhar_card', 'aadhar_card_expiry_date',
              'pan_card', 'pan_card_expiry_date',
              'gst_licence', 'gst_licence_expiry_date',
              'shop_act', 'shop_act_expiry_date',
              'trade_licence', 'trade_licence_expiry_date',
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
