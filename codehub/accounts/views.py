from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User # Using Django's User for sessions
import requests
import os # Import os to access environment variables
import random
import time
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
# Firebase Admin SDK (if you still need it for user creation)
from firebase_admin import auth

def generate_otp(length=6):
    """Generates a random 6-digit OTP."""
    return str(random.randint(10**(length-1), (10**length) - 1))

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # 1. Create user in Firebase
            user_record = auth.create_user(
                email=email,
                password=password,
                display_name=username
            )
            # 2. Create a corresponding Django User to handle sessions
            user = User.objects.create_user(username=user_record.uid, email=email, first_name=username)
            return redirect("login")

        except Exception as e:
            # Provide the error to the user
            return render(request, "registration.html", {"error": str(e)})

    return render(request, "registration.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Get the API key securely from the environment variables
        api_key = os.getenv("FIREBASE_WEB_API_KEY")
        rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {"email": email, "password": password, "returnSecureToken": True}

        try:
            response = requests.post(rest_api_url, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                # User is authenticated with Firebase, now log them into Django
                uid = response_data.get("localId")
                try:
                    # Find the corresponding Django user by the UID we stored as username
                    user = User.objects.get(username=uid)
                    login(request, user) # This creates the session
                    return redirect("dashboard")
                except User.DoesNotExist:
                    return render(request, "login.html", {"error": "User not found in our system. Please register."})
            else:
                # The login failed, show the error from Firebase
                error_message = response_data.get("error", {}).get("message", "Invalid credentials.")
                return render(request, "login.html", {"error": error_message})

        except requests.exceptions.RequestException:
            return render(request, "login.html", {"error": "Network error. Could not connect to authentication service."})

    return render(request, "login.html")

@login_required(login_url='/accounts/login/')
def profile_view(request):
    """
    Displays the user's profile page.
    """
    return render(request, 'profile.html')

def logout_view(request):
    logout(request) # Clears the Django session
    return redirect('index')

def forgot_password_view(request):
    """
    Renders the page where users can request a password reset.
    """
    return render(request, 'forgotpassword.html')

@csrf_exempt
def send_otp_view(request):
    """
    Handles the POST request from forgotpassword.html.
    Finds the user, generates OTP, saves to session, and sends email.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required.'})

        try:
            # 1. Find the user in FIREBASE AUTH (the 'codehubdebug' way)
            user = auth.get_user_by_email(email)
            
            # 2. Generate and store OTP in session
            otp = generate_otp()
            request.session['reset_otp'] = otp
            request.session['otp_timestamp'] = time.time()
            request.session['reset_email'] = email
            request.session['reset_uid'] = user.uid # Store the Firebase UID!

            # 3. Send the email with the OTP
            send_mail(
                'Your CodeHub Password Reset Code',
                f'Your OTP code is: {otp}\nIt will expire in 5 minutes.',
                'noreply@codehub.com', # Configure this in settings.py
                [email],
                fail_silently=False,
            )
            
            # 4. Redirect to the 'verify_otp' page
            return JsonResponse({'success': True, 'redirect_url': reverse('verify_otp')})
            
        except auth.UserNotFoundError:
            return JsonResponse({'success': False, 'message': 'User with this email not found.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request.'})


# STEP 2: RENDER THE "VERIFY OTP" PAGE
def verify_otp_view(request):
    """
    Renders the page for the user to enter their OTP.
    """
    email = request.session.get('reset_email')
    if not email:
        return redirect('forgot_password') # No email in session, start over
    
    return render(request, 'verify_otp.html', {'email': email})

# STEP 2b: API TO CHECK THE OTP
@csrf_exempt
def check_otp_view(request):
    """
    Handles the POST request from verify_otp.html.
    Checks if the OTP is correct and not expired.
    """
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        
        session_otp = request.session.get('reset_otp')
        session_time = request.session.get('otp_timestamp')
        
        if not session_otp or not session_time:
            return JsonResponse({'success': False, 'message': 'Session expired. Please request a new code.'})
            
        # Check for OTP expiry (5 minutes = 300 seconds)
        if time.time() - session_time > 300:
            # Clear session keys on expiry
            request.session.pop('reset_otp', None)
            request.session.pop('otp_timestamp', None)
            return JsonResponse({'success': False, 'message': 'OTP expired. Please request a new one.'})
            
        # Check if OTP matches
        if user_otp == session_otp:
            # OTP is correct! Mark as verified in session.
            request.session['otp_verified'] = True
            return JsonResponse({'success': True, 'redirect_url': reverse('reset_password')})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid OTP code.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

# STEP 3: RENDER THE "NEW PASSWORD" PAGE
def reset_password_view(request):
    """
    Renders the final page to enter a new password.
    """
    if not request.session.get('otp_verified'):
        return redirect('forgot_password') # Not verified, start over
    
    return render(request, 'reset_password.html')

# STEP 3b: API TO FINALIZE THE PASSWORD RESET
@csrf_exempt
def finalize_reset_view(request):
    """
    Handles the POST request from reset_password.html.
    Updates the password in Firebase Auth.
    """
    if request.method == 'POST':
        if not request.session.get('otp_verified'):
            return JsonResponse({'success': False, 'message': 'Not authorized. Please verify OTP.'})

        new_password = request.POST.get('new_password')
        uid = request.session.get('reset_uid') # Get UID we stored in Step 1

        if not new_password or not uid:
            return JsonResponse({'success': False, 'message': 'Session error. Please start over.'})
            
        try:
            # THIS IS THE KEY:
            # Use Firebase Admin SDK to update the password in Firebase Auth
            auth.update_user(uid, password=new_password)
            
            # Clear all reset-related session keys
            request.session.pop('reset_otp', None)
            request.session.pop('otp_timestamp', None)
            request.session.pop('reset_email', None)
            request.session.pop('reset_uid', None)
            request.session.pop('otp_verified', None)
            
            # Send user to login
            return JsonResponse({'success': True, 'redirect_url': reverse('login')})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error updating password: {str(e)}'})
            
    return JsonResponse({'success': False, 'message': 'Invalid request.'})
