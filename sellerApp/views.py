from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import *
import random
from django.views import View
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django_countries import Countries
from datetime import timedelta
from django.utils import timezone


class BuyerPage(View):
    def get(self, request):
        sellers = Seller.objects.filter(user__is_active=True)

        context = {
            'sellers': sellers
        }

        return render(request, 'seller/buyer_page.html', context)


# edit_seller_profile
class edit_seller_profile(View):
    def get(self, request):
        seller = Seller.objects.filter(user=request.user).first()
        if seller:
            team_members = TeamMember.objects.filter(seller=seller).first()
            seller_bank = SellerBank.objects.filter(seller=seller).first()
            product_upload_method = ProductUploadMethod.objects.filter(seller=seller).first()
            documents = Document.objects.filter(user=request.user).first()

            country_choices = [(code, name) for code, name in list(Countries())]
            default_country = seller.seller_country if seller.seller_country else 'IN'

            context = {
                'seller': seller,
                'team_members': team_members,
                'seller_bank': seller_bank,
                'product_upload_method': product_upload_method,
                'documents': documents,
                'countries': country_choices,
                'default_country': default_country,
            }
            return render(request, 'seller/edit_seller_profile.html', context)
        else:
            messages.error(request, 'Seller profile not found.')
            return redirect('seller_profile')

    def post(self, request):
        seller = Seller.objects.filter(user=request.user).first()

        if seller:
            try:
                user = request.user
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.phone_number = request.POST.get('phone_number')
                user.alternate_mobile_number = request.POST.get('alternate_mobile_number')

                new_email = request.POST.get('email')
                if new_email and new_email != user.email:
                    user.email = new_email
                    user.username = new_email
                    user.save()

                    messages.success(request, "Email changed successfully. Please log in with your new email.")
                    logout(request)
                    return redirect('seller_login')

                user.save()

                seller.business_name = request.POST.get('business_name')
                seller.business_registration_number = request.POST.get('business_registration_number')
                seller.business_type = request.POST.get('business_type')
                seller.date_of_business_establishment = request.POST.get('date_of_business_establishment')
                seller.address_line_1 = request.POST.get('address_line_1')
                seller.address_line_2 = request.POST.get('address_line_2')
                seller.city = request.POST.get('city')
                seller.state = request.POST.get('state')
                seller.seller_country = request.POST.get('seller_country')
                seller.postal_code = request.POST.get('postal_code')
                seller.website_url = request.POST.get('website_url')
                seller.business_category = request.POST.get('business_category')
                seller.brand_information = request.POST.get('brand_information')

                seller.save()

                team_members = TeamMember.objects.filter(seller=seller).first()
                team_members.full_name_1 = request.POST.get('full_name_1')
                team_members.teammate_email_1 = request.POST.get('teammate_email_1')
                team_members.teammate_role_1 = request.POST.get('teammate_role_1')

                team_members.full_name_2 = request.POST.get('full_name_2')
                team_members.teammate_email_2 = request.POST.get('teammate_email_2')
                team_members.teammate_role_2 = request.POST.get('teammate_role_2')

                team_members.full_name_3 = request.POST.get('full_name_3')
                team_members.teammate_email_3 = request.POST.get('teammate_email_3')
                team_members.teammate_role_3 = request.POST.get('teammate_role_3')

                team_members.full_name_4 = request.POST.get('full_name_4')
                team_members.teammate_email_4 = request.POST.get('teammate_email_4')
                team_members.teammate_role_4 = request.POST.get('teammate_role_4')

                team_members.full_name_5 = request.POST.get('full_name_5')
                team_members.teammate_email_5 = request.POST.get('teammate_email_5')
                team_members.teammate_role_5 = request.POST.get('teammate_role_5')

                team_members.save()

                seller_bank = SellerBank.objects.filter(seller=seller).first()
                seller_bank.bank_name = request.POST.get('bank_name')
                seller_bank.bank_account_number = request.POST.get('bank_account_number')
                seller_bank.swift_bic_code = request.POST.get('swift_bic_code')
                seller_bank.account_holder_name = request.POST.get('account_holder_name')
                seller_bank.bank_address = request.POST.get('bank_address')

                seller_bank.save()

                product_upload_method = ProductUploadMethod.objects.filter(seller=seller).first()
                product_upload_method.upload_method = request.POST.get('upload_method')
                product_upload_method.platform_type = request.POST.get('platform_type')
                product_upload_method.api_keys = request.POST.get('api_keys')
                product_upload_method.technical_contact_name = request.POST.get('technical_contact_name')
                product_upload_method.technical_contact_email = request.POST.get('technical_contact_email')
                product_upload_method.technical_contact_phone = request.POST.get('technical_contact_phone')
                product_upload_method.preferred_shipping_method = request.POST.get('preferred_shipping_method')

                product_upload_method.save()

                documents = Document.objects.filter(user=request.user).first()
                if request.FILES.get('business_registration_document'):
                    documents.business_registration_document = request.FILES['business_registration_document']
                if request.POST.get('business_registration_document_expiry_date'):
                    documents.business_registration_document_expiry_date = request.POST.get(
                        'business_registration_document_expiry_date')

                if request.FILES.get('tax_identification_document'):
                    documents.tax_identification_document = request.FILES['tax_identification_document']
                if request.POST.get('tax_identification_document_expiry_date'):
                    documents.tax_identification_document_expiry_date = request.POST.get(
                        'tax_identification_document_expiry_date')

                if request.FILES.get('proof_of_business_address'):
                    documents.proof_of_business_address = request.FILES['proof_of_business_address']
                if request.POST.get('proof_of_business_address_expiry_date'):
                    documents.proof_of_business_address_expiry_date = request.POST.get(
                        'proof_of_business_address_expiry_date')

                if request.FILES.get('authorized_signatory_id'):
                    documents.authorized_signatory_id = request.FILES['authorized_signatory_id']
                if request.POST.get('authorized_signatory_id_expiry_date'):
                    documents.authorized_signatory_id_expiry_date = request.POST.get(
                        'authorized_signatory_id_expiry_date')

                documents.save()

                messages.success(request, 'Profile updated successfully.')
                return redirect('seller_profile')

            except Exception as e:
                messages.error(request, f"An error occurred while saving your profile: {str(e)}")
                return redirect('edit_seller_profile')

        else:
            messages.error(request, 'Seller profile not found.')
            return redirect('seller_profile')


class seller_signup_form(View):
    def get(self, request):
        country_choices = [(code, name) for code, name in list(Countries())]
        default_country = 'IN'
        context = {
            'countries': country_choices,
            'default_country': default_country,
        }
        return render(request, 'seller/seller_signup_form.html', context)

    def post(self, request):
        countries = Countries()
        country_choices = [(name, name) for code, name in list(countries)]

        try:
            # User data-------------------------------------------
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            alternate_mobile_number = request.POST.get('alternate_mobile_number')

            # Team member data-------------------------------------
            full_name_1 = request.POST.get('full_name_1')
            teammate_email_1 = request.POST.get('teammate_email_1')
            teammate_role_1 = request.POST.get('teammate_role_1')

            full_name_2 = request.POST.get('full_name_2')
            teammate_email_2 = request.POST.get('teammate_email_2')
            teammate_role_2 = request.POST.get('teammate_role_2')

            full_name_3 = request.POST.get('full_name_3')
            teammate_email_3 = request.POST.get('teammate_email_3')
            teammate_role_3 = request.POST.get('teammate_role_3')

            full_name_4 = request.POST.get('full_name_4')
            teammate_email_4 = request.POST.get('teammate_email_4')
            teammate_role_4 = request.POST.get('teammate_role_4')

            full_name_5 = request.POST.get('full_name_5')
            teammate_email_5 = request.POST.get('teammate_email_5')
            teammate_role_5 = request.POST.get('teammate_role_5')

            # Seller data-------------------------------------------
            business_name = request.POST.get('business_name')
            business_type = request.POST.get('business_type')
            business_registration_number = request.POST.get('business_registration_number')
            date_of_business_establishment = request.POST.get('date_of_business_establishment')

            address_line_1 = request.POST.get('address_line_1')
            address_line_2 = request.POST.get('address_line_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            seller_country = request.POST.get('seller_country')
            postal_code = request.POST.get('postal_code')

            website_url = request.POST.get('website_url')
            business_category = request.POST.get('business_category')
            brand_information = request.POST.get('brand_information')

            # Bank data----------------------------------------------
            bank_name = request.POST.get('bank_name')
            bank_account_number = request.POST.get('bank_account_number')
            swift_bic_code = request.POST.get('swift_bic_code')
            account_holder_name = request.POST.get('account_holder_name')
            bank_address = request.POST.get('bank_address')

            # Document data-------------------------------------------
            business_registration_document = request.FILES.get('business_registration_document')
            business_registration_document_expiry_date = request.POST.get('business_registration_document_expiry_date')

            tax_identification_document = request.FILES.get('tax_identification_document')
            tax_identification_document_expiry_date = request.POST.get('tax_identification_document_expiry_date')

            proof_of_business_address = request.FILES.get('proof_of_business_address')
            proof_of_business_address_expiry_date = request.POST.get('proof_of_business_address_expiry_date')

            authorized_signatory_id = request.FILES.get('authorized_signatory_id')
            authorized_signatory_id_expiry_date = request.POST.get('authorized_signatory_id_expiry_date')

            # Product upload method data----------------------------------
            upload_method = request.POST.get('upload_method')
            platform_type = request.POST.get('platform_type')
            api_keys = request.POST.get('api_keys')
            technical_contact_name = request.POST.get('technical_contact_name')
            technical_contact_email = request.POST.get('technical_contact_email')
            technical_contact_phone = request.POST.get('technical_contact_phone')
            preferred_shipping_method = request.POST.get('preferred_shipping_method')

            # Terms and conditions-------------------------------------------
            agreement = request.POST.get('agreement') == 'on'
            signature = request.POST.get('signature') == 'on'
            date_signed = request.POST.get('date_signed')

            # Validations
            validation_errors = []

            if User.objects.filter(email=email).exists():
                validation_errors.append('Email already taken.')

            if User.objects.filter(phone_number=phone_number).exists():
                validation_errors.append('Phone number already taken.')

            if Seller.objects.filter(business_registration_number=business_registration_number).exists():
                validation_errors.append('Business Registration number already taken.')

            if Seller.objects.filter(business_name=business_name).exists():
                validation_errors.append('Business name already taken.')

            if validation_errors:
                for error in validation_errors:
                    messages.error(request, error)
                return render(request, 'seller/seller_signup_form.html', {
                    'countries': country_choices,
                    'default_country': 'IN'
                })

            # Create User
            user = User(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                alternate_mobile_number=alternate_mobile_number,
                is_seller=True,
                is_active=False
            )
            user.save()

            # Create Seller
            seller = Seller(
                user=user,
                business_name=business_name,
                business_type=business_type,
                business_registration_number=business_registration_number,
                date_of_business_establishment=date_of_business_establishment,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                seller_country=seller_country,
                postal_code=postal_code,
                website_url=website_url,
                business_category=business_category,
                brand_information=brand_information,
            )
            seller.save()

            # Create and save Team member
            team_member = TeamMember(
                seller=seller,

                full_name_1=full_name_1,
                teammate_email_1=teammate_email_1,
                teammate_role_1=teammate_role_1,

                full_name_2=full_name_2,
                teammate_email_2=teammate_email_2,
                teammate_role_2=teammate_role_2,

                full_name_3=full_name_3,
                teammate_email_3=teammate_email_3,
                teammate_role_3=teammate_role_3,

                full_name_4=full_name_4,
                teammate_email_4=teammate_email_4,
                teammate_role_4=teammate_role_4,

                full_name_5=full_name_5,
                teammate_email_5=teammate_email_5,
                teammate_role_5=teammate_role_5,
            )
            team_member.save()

            # Create and save Seller bank
            seller_bank = SellerBank(
                seller=seller,
                bank_name=bank_name,
                bank_account_number=bank_account_number,
                swift_bic_code=swift_bic_code,
                account_holder_name=account_holder_name,
                bank_address=bank_address,
            )
            seller_bank.save()

            # Create and save Terms and conditions
            terms_and_conditions = TermsAndConditions(
                seller=seller,
                agreement=agreement,
                signature=signature,
                date_signed=date_signed,
            )
            terms_and_conditions.save()

            # Create and save Product upload method
            product_upload_method = ProductUploadMethod(
                seller=seller,
                upload_method=upload_method,
                platform_type=platform_type,
                api_keys=api_keys,
                technical_contact_name=technical_contact_name,
                technical_contact_email=technical_contact_email,
                technical_contact_phone=technical_contact_phone,
                preferred_shipping_method=preferred_shipping_method,
            )
            product_upload_method.save()

            # Create and save Document
            document = Document(
                user=seller.user,
                business_registration_document=business_registration_document,
                business_registration_document_expiry_date=business_registration_document_expiry_date,
                tax_identification_document=tax_identification_document,
                tax_identification_document_expiry_date=tax_identification_document_expiry_date,
                proof_of_business_address=proof_of_business_address,
                proof_of_business_address_expiry_date=proof_of_business_address_expiry_date,
                authorized_signatory_id=authorized_signatory_id,
                authorized_signatory_id_expiry_date=authorized_signatory_id_expiry_date,
            )
            document.save()

            # Send activation email
            self.send_email(email, first_name, last_name, user)

            messages.success(request, 'Signup successful! Please check your email to activate your account.')
            return redirect('seller_login')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'seller/seller_signup_form.html', {
                'countries': country_choices,
                'default_country': 'India'
            })

    def send_email(self, recipient_email, first_name, last_name, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request)
        activation_link = f"http://{current_site.domain}/seller/activate/{uid}/{token}/"

        html_message = render_to_string('seller/seller_activation_email.html', {
            'first_name': first_name,
            'last_name': last_name,
            'activation_link': activation_link,
        })
        plain_message = strip_tags(html_message)

        subject = 'Activate Your Account'
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            plain_message,
            from_email,
            [recipient_email],
            html_message=html_message,
            fail_silently=False,
        )


def send_otp(email):
    otp = random.randint(100000, 999999)
    send_mail(
        'Your OTP Code',
        f'Your OTP code is {otp}',
        'DEFAULT_FROM_EMAIL',
        [email],
        fail_silently=False,
    )
    return otp


class seller_login(View):
    def get(self, request):
        return render(request, 'seller/seller_login.html')

    def post(self, request):
        email = request.POST.get('email')
        otp = request.POST.get('otp')

        if 'send_otp' in request.POST:
            user = User.objects.filter(email=email).first()
            if user:
                if user.is_active:
                    otp = send_otp(email)
                    request.session['otp'] = otp
                    request.session['email'] = email
                    messages.success(request, 'OTP sent to your email.')
                    return redirect('seller_profile')
                else:
                    messages.error(request, 'Your account is not activated. Please activate your account first from '
                                            'your mail.')
            else:
                messages.error(request, 'Invalid email!')

        elif 'login' in request.POST:
            user = User.objects.filter(email=request.session.get('email')).first()
            if user:
                if not user.is_active:
                    messages.error(request, 'Your account is not activated. Please activate your account first.')
                    return redirect('seller_account_activation')

                if str(otp) == str(request.session.get('otp')):
                    login(request, user)
                    print(f"User {user.email} logged in successfully.")
                    return redirect('seller_profile')
                else:
                    messages.error(request, 'Invalid OTP!')
            else:
                messages.error(request, 'Invalid email!')

        return render(request, 'seller/seller_login.html')


class seller_account_activation(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, 'Your account has been activated successfully! You can now log in.')
            return redirect('seller_login')
        else:
            messages.error(request, 'Activation link is invalid or has expired!')
            return redirect('seller_signup_form')


def seller_logout(request):
    logout(request)
    return redirect('seller_login')


class seller_profile(LoginRequiredMixin, View):
    login_url = 'seller_login'

    def get(self, request):
        seller = Seller.objects.filter(user=request.user).first()
        documents = Document.objects.filter(user=request.user).first()
        team_member = TeamMember.objects.filter(seller=seller).first()
        product_upload_method = ProductUploadMethod.objects.filter(seller=seller).first()
        seller_bank = SellerBank.objects.filter(seller=seller).first()

        is_approved = documents.is_approved if documents else False

        self.check_document_expiry(documents, seller)

        context = {
            'seller': seller,
            'documents': documents,
            'team_member': team_member,
            'product_upload_method': product_upload_method,
            'seller_bank': seller_bank,
            'is_approved': is_approved,
        }

        return render(request, 'seller/seller_profile.html', context)

    def post(self, request):
        seller = Seller.objects.get(user=request.user)

        share_preferences = {

            # share business information

            'share_business_name': request.POST.get('share_business_name') == 'on',
            'share_registration_number': request.POST.get('share_registration_number') == 'on',
            'share_business_type': request.POST.get('share_business_type') == 'on',

            # share address

            'share_address_line_1': request.POST.get('share_address_line_1') == 'on',
            'share_address_line_2': request.POST.get('share_address_line_2') == 'on',
            'share_city': request.POST.get('share_city') == 'on',
            'share_state': request.POST.get('share_state') == 'on',
            'share_seller_country': request.POST.get('share_seller_country') == 'on',
            'share_postal_code': request.POST.get('share_postal_code') == 'on',
        }

        if not any(share_preferences.values()):
            messages.error(request, 'Please select at least one preference.')
            return redirect('seller_profile')

        for key, value in share_preferences.items():
            setattr(seller, key, value)

        seller.save()
        messages.success(request, 'Your sharing preferences have been updated successfully.')
        return redirect('seller_profile')

    def check_document_expiry(self, documents, seller):
        if documents:
            today = timezone.now().date()
            one_month_from_today = today + timedelta(days=30)

            expiry_dates = {
                'Business Registration Document': documents.business_registration_document_expiry_date,
                'Tax Identification Document': documents.tax_identification_document_expiry_date,
                'Proof of Business Address': documents.proof_of_business_address_expiry_date,
                'Authorized Signatory ID': documents.authorized_signatory_id_expiry_date,
            }

            expiring_documents = []
            for doc_name, expiry_date in expiry_dates.items():
                if expiry_date and today < expiry_date <= one_month_from_today:
                    expiring_documents.append(doc_name)

            if expiring_documents:
                self.send_expiry_notification(seller.user.email, seller.business_name, expiring_documents)

    def send_expiry_notification(self, recipient_email, business_name, document_names):

        subject = 'Document Expiry Notice'
        document_list = ', '.join(document_names)
        message = (
            f'Dear {business_name},\n\n'
            f'The following documents are expiring within the next 30 days: {document_list}. '
            'Please update the documents.\n\n'
            'Thank you,\nXYZ Company'
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject,
            message,
            from_email,
            [recipient_email],
            fail_silently=False,
        )


def seller_add_products(request):
    return render(request, 'seller/seller_add_products.html')
