"""checkNface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin', admin.site.urls),
    path('main', views.home, name='main'),
    # Admin Dashboard Routes/Urls
    path('dashboard/', views.dashboard, name='dashboard'),
    path('checkin/', views.read_checkin, name='checkin'),
    path('checkout/', views.read_checkout, name='checkout'),
    path('edit_employees/', views.edit_employees, name='edit_employees'),
    path('general_reports/', views.general_reports, name='general_reports'),
    path('help/', views.helps, name='helps'),
    path('manage_admins/', views.register, name='manage_admins'),
    path('edit_admins/<int:id>', views.edit_admins),
    path('update_admins/<int:id>', views.update_admins),
    path('delete_admins/<int:id>', views.destroy_admins),
    path('manage_employees/', views.read, name='manage_employees'),
    path('add_employees/', views.new, name='add_employees'),
    path('add_new_employee', views.create, name='add_new_employee'),
    path('edit/<int:id>', views.edit),
    path('update/<int:id>', views.update),
    path('delete/<int:id>', views.destroy),
    path('notes/', views.notes, name='notes'),
    path('admin_contact_us/', views.contactus_read, name='admin_contact_us'),

    # Main Website Routes/Urls
    path(r'', views.homepage),
    path('homepage/', views.homepage, name='homepage'),
    path('about-us/', views.aboutus, name='about-us'),
    path('our-mission/', views.ourmission, name='our-mission'),
    path('how-it-works/', views.howitworks, name='how-it-works'),

    # Contact-us urls
    path('contact-us/', views.contactus, name='contact-us'),
    path('contact-us-read/', views.contactus_read, name='contact-us-read'),
    path('add_contact/', views.new_contact, name='add_contact'),
    path('add_new_contact', views.create_contact, name='add_new_contact'),
    # Request a demo urls
    path('request-demo/', views.requestdemo, name='request-demo'),
    path('request-demo-read/', views.requestdemo_read, name='request-demo_read'),
    path('add_request/', views.new_request, name='add_request'),
    path('add_new_request', views.create_request, name='add_new_request'),

    # Register Routes/Urls
    # path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_page/', views.register_page, name='register_page'),
    # Attendance AI system Routes/Urls
    path('attendance/', views.attendance, name='attendance'),
    path('attendance_check_in/', views.attendance_check_in, name='attendance_check_in'),
    path('attendance_check_out/', views.attendance_check_out, name='attendance_check_in_out'),
    # login
    path('', include("django.contrib.auth.urls")),
    # Virtual Assistance
    path('virtual_assistance/', views.virtual_assistance, name='virtual_assistance'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
