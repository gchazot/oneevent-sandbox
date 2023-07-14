"""oneevent_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import user_profile, user_disconnect_social_auth

urlpatterns = [
    path('ping/', lambda *args, **kwargs: HttpResponse("pong")),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', user_profile, name='user_profile'),
    path('accounts/profile/<backend>/',
         user_disconnect_social_auth,
         name='user_disconnect_social_auth'),
    path('', include('social_django.urls', namespace='social')),
    path('', include('oneevent.urls')),
]

