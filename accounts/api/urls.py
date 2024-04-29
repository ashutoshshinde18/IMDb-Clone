from django.contrib import admin
from django.urls import path
from accounts.api.views import logout_view, login_success_view, login_view, registration_view, RegisterView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('registration-page/', registration_view, name='register-page'),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_success_view, name='login'),
    path('login-page/', login_view, name='login-page'),
    path('logout/', logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)