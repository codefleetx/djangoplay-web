from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'get_company', 'created_at')
    search_fields = ('name', 'email', 'company')

    def get_company(self, obj):
        return ", ".join([company.name for company in obj.companies.all()])
    get_company.short_description = "Company"   # Column header in admin
