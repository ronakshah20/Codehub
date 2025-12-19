from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    """
    Renders the main landing page.
    If the user is already authenticated, it redirects them to the dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    # If the user is not logged in, show the normal homepage
    return render(request, 'index.html')
