from django.urls import path
from app.views import *
from home.views import *
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm,CustomSetPasswordForm


# urls.py
urlpatterns = [
    path("",index,name='index'),
    # --SINGUP AND LOGIN--
    path("login/",handlelogin,name='login'),
    path("signup/",handlesignup,name='signup'),
    path("logout/",handlelogout,name='logout'),
    path("verify_user/<str:code>/",verify_user,name='verify_user'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        form_class=CustomPasswordResetForm,  
        template_name='forgot_password.html', 
        email_template_name='password_reset_email.html',  
        subject_template_name='password_reset_subject.txt',  
    ), name='reset_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='forgot_password.html',  
        form_class=CustomSetPasswordForm, 
    ), name='password_reset_confirm'),
    path('reset_password_done/', reset_password_done, name='reset_password_done'),
    path('reset_password_complete/', password_reset_complete, name='password_reset_complete'),
    # --USER DASHBOARD AND PROFILE--
    path("home",home,name='home'),
    path("watchlist",watchlist,name='watchlist'),
    path('search/', search_instruments, name='search_instruments'),
    path("add_watchlist",add_watchlist,name='add_watchlist'),
    path("create_watchlist",create_watchlist,name='create_watchlist'),
    path("delete_stock",delete_stock,name='delete_stock'),
    path("delete_symbol/<str:symbol>",delete_symbol,name='delete_symbol'),
    path("place_order",place_order,name='place_order'),
    path("orders",orders,name='orders'),
    path("portfolio",portfolio,name='portfolio'),
    path("profile",profile,name='profile'),
    path("trends",trends,name='trends'),
    path("trade_charges",trade_charges,name='trade_charges'),
    path("pnl",pnl,name='pnl'),
    path("transactions",transactions,name='transactions'),
    path("withdraw",withdraw,name='withdraw'),
    path("add-funds",addFunds,name='addFunds'),
    path("performance",performance,name='performance'),
    path("kyc",kyc,name='kyc'),
    # Payment Gateway
    path("payment-status/<str:order_id>",paymentStatus,name='paymentStatus'),
    # PAY U
    path('payment/success/', payment_success, name='payment_success'),
    path('payment/failure/', payment_failure, name='payment_failure'),
    # --PAGES--
    path("about",about,name='about'),
    path("disclaimer",disclaimer,name='disclaimer'),
    path("contact",contact,name='contact'),
    # POLICY
    path("privacypolicy",privacypolicy,name='privacypolicy'),
    path("refundpolicy",refundpolicy,name='refundpolicy'),
    #  WATCHLIST
    path("add_to_watchlist",add_to_watchlist,name='add_to_watchlist'),
    path("upstox_cred/<str:secret>",upstox_cred,name='upstox_cred'),
    # TRANSACTIONS
    path("cancel_order/<str:order_id>",cancel_order,name='cancel_order'),
    path("cancelorder/<str:order_id>",cancelorder,name='cancelorder'),
    # Admin Urls
    path("closepos/<str:id>",closepos,name='closepos'),
    path("close_position",close_position,name='close_position'),
    path("update_symbols",update_symbols,name='update_symbols'),
]
