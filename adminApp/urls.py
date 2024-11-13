from django.urls import path
from .views import *

urlpatterns = [

    # Need design for this
    path('buyers/', BuyerPage.as_view(), name='buyer_page'),


    # template rendering done===================================================================

    path('', seller_login.as_view(), name='seller_login'),
    path('seller/signup_form/', seller_signup_form.as_view(), name='seller_signup_form'),
    path('logout/', seller_logout, name='seller_logout'),
    path('seller/profile/', seller_profile.as_view(), name='seller_profile'),
    path('seller/activate/<uidb64>/<token>/', seller_account_activation.as_view(), name='seller_account_activation'),
    path('seller/profile/edit/', edit_seller_profile.as_view(), name='edit_seller_profile'),
    path('seller/add/products/', seller_add_products, name="seller_add_products"),
    path('buyers/', BuyerPage.as_view(), name='buyer_page'),                        # Need design for this

]

