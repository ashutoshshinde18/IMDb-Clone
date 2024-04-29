from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from accounts.api.serializers import RegistrationSerializer
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def registration_view(request):
    # Logic for registration view
    return render(request, 'registration.html')




def login_success_view(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Obtain the token using obtain_auth_token
        response = obtain_auth_token(request)
        # Get the username and password from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Manually create a session for the user
            login(request, user)
            print(user,'--->user 1')
            # Set session data upon successful login
            # Set session data upon successful login
            request.session['username'] = user.username
            
            # Generate or get refresh token
            refresh_token, _ = Token.objects.get_or_create(user=user)
            
            # Redirect to the home page
            return HttpResponseRedirect(reverse('home'))
            
        else:
            # Authentication failed, return response obtained from obtain_auth_token
            messages.error(request, 'Invalid username or password.')
            # Redirect back to the login page
            return redirect(reverse('login-page'))
    else:
        # Redirect to login page if request method is not POST
        return redirect(reverse('login-page'))
    

def login_view(request):
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login-page')  # Redirect to login page after logout
    
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # token, _ = Token.objects.get_or_create(user=serializer.instance)
        return redirect('login-page')

# def register(request):
#     if request.method == 'POST':
#         serializer = RegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, _ = Token.objects.get_or_create(user=user)
#             return render(request,'login.html')
#         return redirect(reverse('home'))