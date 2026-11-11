from django.contrib import admin
from .models import AuditResult


@admin.register(AuditResult)
class AuditResultAdmin(admin.ModelAdmin):
    list_display = ['site_url', 'audit_date', 'status']
    list_filter = ['status']
    search_fields = ['site_url']
