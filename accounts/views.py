from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

# Custom login view to handle login form rendering
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))  # Redirect to a protected page after login
            else:
                form.add_error(None, "Invalid credentials")
        else:
            form.add_error(None, "Invalid credentials")

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Custom logout view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))  # Redirect to login page after logout

def homepage_view(request):
    return render(request,'base.html')

def codeeditor_view(request):
    return render(request,'accounts/codeeditor.html')