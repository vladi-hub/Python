"""homeinv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,reverse
from django.utils.http import urlquote 
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from homeinventory import views

urlpatterns = [
    path('admin/', admin.site.urls),
	
	path('hi/main/<slug:cmd>/', views.main, name='main'),
	path('hi/dashboard/', views.home, name='home'),
	path('hi/locations/', views.locations, name='locations'),
	path('hi/assets/', views.asset, name='asset'),
	path('hi/services/', views.service, name='service'),
	path('hi/user/', views.user),
    path('hi/location/<int:id>/', views.location_id, name='locationsview'),
    path('hi/asset/<int:id>/<int:location_id>/', views.asset_id, name='assetview'),
	path('hi/service/<int:id>/<int:location_id>/', views.service_id, name='serviceview'),
	
	#path('hi/login/', auth_views.login,{'template_name':  'login.html'}, name='login'),

	path('hi/login/', views.loginUser, name='loginUser'),
    path('hi/logout/', auth_views.logout,{'template_name': 'logout.html'}, name='logout'),
	
	path('hi/signup/', views.signup, name='signup'),
	path('hi/account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('hi/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
		
		
	path('hi/password_reset/', auth_views.password_reset, name='password_reset'),
    path('hi/password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('hi/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('hi/reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),	
]
