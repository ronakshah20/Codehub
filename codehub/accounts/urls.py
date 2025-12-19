# codehubdebug/accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),

    # --- NEW 3-STEP PASSWORD RESET FLOW ---

    # Step 1: Page to enter email
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    
    # Step 1b: API for sending the OTP code
    path("api/send-otp/", views.send_otp_view, name="send_otp"),

    # Step 2: Page to enter the OTP
    path("verify-otp/", views.verify_otp_view, name="verify_otp"),
    
    # Step 2b: API for checking the OTP
    path("api/check-otp/", views.check_otp_view, name="check_otp"),

    # Step 3: Page to enter the new password
    path("reset-password/", views.reset_password_view, name="reset_password"),
    
    # Step 3b: API for finalizing the password change
    path("api/finalize-reset/", views.finalize_reset_view, name="finalize_reset"),
]
