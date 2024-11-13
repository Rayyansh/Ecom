from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
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
import re
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django_countries import Countries, countries
from datetime import timedelta
from django.utils import timezone


class BuyerPage(View):
    def get(self, request):
        sellers = Seller.objects.filter(user__is_active=True)

        context = {
            'sellers': sellers
        }

        return render(request, 'seller/buyer_page.html', context)


# template rendering done===================================================================
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


def seller_add_products(request):
    return render(request, 'seller/seller_add_products.html')


def seller_logout(request):
    logout(request)
    return redirect('seller_login')


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
            # User data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone_number')
            country = request.POST.get('country')

            # Profile photo
            profile_photo = request.FILES.get('profile_photo')

            # Seller data
            business_name = request.POST.get('business_name')
            registration_number = request.POST.get('registration_number')
            business_type = request.POST.get('business_type')
            tax_identification_number = request.POST.get('tax_identification_number')

            bank_name = request.POST.get('bank_name')
            bank_account_number = request.POST.get('bank_account_number')
            bank_ifsc_code = request.POST.get('bank_ifsc_code')
            bank_branch = request.POST.get('bank_branch')

            # Document data
            aadhar_card = request.FILES.get('aadhar_card')
            aadhar_card_expiry_date = request.POST.get('aadhar_card_expiry_date')

            pan_card = request.FILES.get('pan_card')
            pan_card_expiry_date = request.POST.get('pan_card_expiry_date')

            gst_licence = request.FILES.get('gst_licence')
            gst_licence_expiry_date = request.POST.get('gst_licence_expiry_date')

            shop_act = request.FILES.get('shop_act')
            shop_act_expiry_date = request.POST.get('shop_act_expiry_date')

            trade_licence = request.FILES.get('trade_licence')
            trade_licence_expiry_date = request.POST.get('trade_licence_expiry_date')

            # Validation
            validation_errors = self.validate_signup_data(
                email, first_name, last_name, gender, address, business_name, registration_number,
                business_type, tax_identification_number, bank_name, bank_account_number,
                bank_ifsc_code, bank_branch
            )

            if validation_errors:
                for error in validation_errors:
                    messages.error(request, error)
                return render(request, 'seller/seller_signup_form.html', {
                    'countries': country_choices,
                    'default_country': 'India'
                })

            # Check if user with this email or phone number already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken.')
                return render(request, 'seller/seller_signup_form.html', {
                    'countries': country_choices,
                    'default_country': 'India'
                })

            if User.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'Phone number already taken.')
                return render(request, 'seller/seller_signup_form.html', {
                    'countries': country_choices,
                    'default_country': 'India'
                })

            # Check if seller with these unique business identifiers already exists
            if Seller.objects.filter(registration_number=registration_number).exists():
                messages.error(request, 'Registration number already taken.')
                return render(request, 'seller/seller_signup_form.html', {
                    'countries': country_choices,
                    'default_country': 'India'
                })

            if Seller.objects.filter(tax_identification_number=tax_identification_number).exists():
                messages.error(request, 'Tax Identification Number already taken.')
                return render(request, 'seller/seller_signup_form.html', {
                    'countries': country_choices,
                    'default_country': 'India'
                })

            # Create and save User
            user = User(
                username=email,
                first_name=first_name,
                last_name=last_name,
                email=email,
                gender=gender,
                address=address,
                phone_number=phone_number,
                country=country,
                profile_photo=profile_photo,
                is_seller=True,
                is_active=False
            )
            user.set_password(request.POST.get('password'))
            user.save()

            # Create and save Seller
            seller = Seller(
                user=user,
                business_name=business_name,
                registration_number=registration_number,
                business_type=business_type,
                tax_identification_number=tax_identification_number,
                bank_name=bank_name,
                bank_account_number=bank_account_number,
                bank_ifsc_code=bank_ifsc_code,
                bank_branch=bank_branch
            )
            seller.save()

            # Create and save Document
            document = Document(
                user=user,
                aadhar_card=aadhar_card,
                aadhar_card_expiry_date=aadhar_card_expiry_date,
                pan_card=pan_card,
                pan_card_expiry_date=pan_card_expiry_date,
                gst_licence=gst_licence,
                gst_licence_expiry_date=gst_licence_expiry_date,
                shop_act=shop_act,
                shop_act_expiry_date=shop_act_expiry_date,
                trade_licence=trade_licence,
                trade_licence_expiry_date=trade_licence_expiry_date,
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

    def validate_signup_data(self, email, first_name, last_name, gender, address, business_name,
                             registration_number, business_type, tax_identification_number,
                             bank_name, bank_account_number, bank_ifsc_code, bank_branch):
        errors = []

        if not all([first_name, last_name, email, gender, address, business_name, registration_number,
                    business_type, tax_identification_number, bank_name, bank_account_number, bank_ifsc_code,
                    bank_branch]):
            errors.append('All fields are required.')

        if first_name and not first_name.isalpha():
            errors.append('First name must contain only characters.')

        if last_name and not last_name.isalpha():
            errors.append('Last name must contain only characters.')

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if email and not re.match(email_regex, email):
            errors.append('Invalid email.')

        if len(bank_ifsc_code) != 11:
            errors.append('Please enter a valid IFSC code.')

        return errors


class seller_profile(LoginRequiredMixin, View):
    login_url = 'seller_login'

    def get(self, request):
        seller = Seller.objects.filter(user=request.user).first()
        documents = Document.objects.filter(user=request.user).first()

        is_approved = documents.is_approved if documents else False

        self.check_document_expiry(documents, seller)

        context = {
            'seller': seller,
            'documents': documents,
            'is_approved': is_approved,
        }

        return render(request, 'seller/seller_profile.html', context)  # Updated template name

    def post(self, request):
        seller = Seller.objects.get(user=request.user)

        share_preferences = {
            'share_business_name': request.POST.get('share_business_name') == 'on',
            'share_address': request.POST.get('share_address') == 'on',
            'share_gender': request.POST.get('share_gender') == 'on',
            'share_phone_number': request.POST.get('share_phone_number') == 'on',
            'share_country': request.POST.get('share_country') == 'on',
            'share_registration_number': request.POST.get('share_registration_number') == 'on',
            'share_business_type': request.POST.get('share_business_type') == 'on',
            'share_tax_identification_number': request.POST.get('share_tax_identification_number') == 'on',
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
                'Aadhar Card': documents.aadhar_card_expiry_date,
                'PAN Card': documents.pan_card_expiry_date,
                'GST License': documents.gst_licence_expiry_date,
                'Shop Act': documents.shop_act_expiry_date,
                'Trade License': documents.trade_licence_expiry_date,
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


class edit_seller_profile(LoginRequiredMixin, View):
    login_url = 'seller_login'

    def get(self, request):
        seller = Seller.objects.filter(user=request.user).first()
        if seller:
            documents = Document.objects.filter(user=request.user).first()

            context = {
                'seller': seller,
                'user': request.user,
                'documents': documents,
                'countries': countries,
            }
            return render(request, 'seller/edit_seller_profile.html', context)
        else:
            messages.error(request, 'Seller profile not found.')
            return redirect('seller_profile')

    def post(self, request):
        seller = Seller.objects.filter(user=request.user).first()

        if seller:
            user = request.user
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.phone_number = request.POST.get('phone_number')
            user.address = request.POST.get('address')
            user.country = request.POST.get('country')

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
            seller.registration_number = request.POST.get('registration_number')
            seller.business_type = request.POST.get('business_type')
            seller.tax_identification_number = request.POST.get('tax_identification_number')

            seller.save()

            documents, created = Document.objects.get_or_create(user=user)

            if request.FILES.get('aadhar_card'):
                documents.aadhar_card = request.FILES['aadhar_card']
            if request.POST.get('aadhar_card_expiry_date'):
                documents.aadhar_card_expiry_date = request.POST.get('aadhar_card_expiry_date')

            if request.FILES.get('pan_card'):
                documents.pan_card = request.FILES['pan_card']
            if request.POST.get('pan_card_expiry_date'):
                documents.pan_card_expiry_date = request.POST.get('pan_card_expiry_date')

            if request.FILES.get('gst_licence'):
                documents.gst_licence = request.FILES['gst_licence']
            if request.POST.get('gst_licence_expiry_date'):
                documents.gst_licence_expiry_date = request.POST.get('gst_licence_expiry_date')

            if request.FILES.get('shop_act'):
                documents.shop_act = request.FILES['shop_act']
            if request.POST.get('shop_act_expiry_date'):
                documents.shop_act_expiry_date = request.POST.get('shop_act_expiry_date')

            if request.FILES.get('trade_licence'):
                documents.trade_licence = request.FILES['trade_licence']
            if request.POST.get('trade_licence_expiry_date'):
                documents.trade_licence_expiry_date = request.POST.get('trade_licence_expiry_date')

            documents.save()

            seller.bank_name = request.POST.get('bank_name')
            seller.bank_account_number = request.POST.get('bank_account_number')
            seller.bank_ifsc_code = request.POST.get('bank_ifsc_code')
            seller.bank_branch = request.POST.get('bank_branch')

            seller.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('seller_profile')
        else:
            messages.error(request, 'Seller profile not found.')
            return redirect('seller_profile')
