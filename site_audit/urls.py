"""
URL configuration for site_audit project.
"""
from django.contrib import admin
from django.urls import path
from audit import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('audit/', views.start_audit, name='start_audit'),
]
