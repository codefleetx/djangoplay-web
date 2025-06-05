from django import forms
from django.contrib import admin
from django.db import models
from django.utils import timezone

from .models import Client, ClientOrganization, Industry, Location, Organization


class ClientOrganizationInlineForm(forms.ModelForm):

    """Form for inline editing of ClientOrganization in the admin."""

    class Meta:
        model = ClientOrganization
        fields = '__all__'
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        """Ensure from_date and to_date are not in the future."""
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        today = timezone.now().date()

        if from_date and from_date > today:
            self.add_error('from_date', 'From date cannot be in the future.')
        if to_date and to_date > today:
            self.add_error('to_date', 'To date cannot be in the future.')

        return cleaned_data


class ClientOrganizationInline(admin.TabularInline):

    """Inline admin for ClientOrganization."""

    model = ClientOrganization
    form = ClientOrganizationInlineForm
    extra = 0
    can_delete = True
    verbose_name = "Previous Business Association"
    verbose_name_plural = "Previous Business Associations"
    fields = ('organization', 'previous_workplace', 'from_date', 'to_date')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """Disable related object actions for organization field."""
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == "organization":
            field.widget.can_change_related = False
            field.widget.can_add_related = False
            field.widget.can_delete_related = False
        return field

    def get_queryset(self, request):
        """Exclude client's current company from queryset."""
        qs = super().get_queryset(request)
        return qs.exclude(organization=models.F('client__current_company'))


@admin.register(ClientOrganization)
class ClientOrganizationInlineAdmin(admin.ModelAdmin):

    """Admin for ClientOrganization."""

    list_display = ('id', 'client', 'organization', 'get_previous_workplace', 'from_date', 'to_date')
    fields = ('client', 'organization', 'get_previous_workplace', 'from_date', 'to_date')
    autocomplete_fields = ['client', 'organization']
    readonly_fields = ['get_previous_workplace']

    def get_previous_workplace(self, obj):
        """Return previous workplace name or '-'."""
        return obj.previous_workplace.name if obj.previous_workplace else "-"
    get_previous_workplace.short_description = "Previous Workplace"


class ClientForm(forms.ModelForm):

    """Form for editing Client in the admin."""

    class Meta:
        model = Client
        fields = '__all__'
        labels = {
            'current_company': 'Current Company:',
            'current_company_joining_day': 'Joining Date:',
            'current_company_location': 'Current Workplace Location:',
        }
        widgets = {
            'current_company_joining_day': forms.DateInput(attrs={'type': 'date'}),
        }


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    """Admin for Client."""

    form = ClientForm
    list_display = ('id', 'name', 'email', 'get_current_company', 'get_past_companies', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'current_company__name', 'past_companies__name', 'industry__name')
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('industry__name', 'created_at')
    ordering = ('-created_at',)
    inlines = [ClientOrganizationInline]
    fields = ('name', 'email', 'phone', 'current_company', 'current_company_joining_day', 'current_company_location', 'industry')

    def get_current_company(self, obj):
        """Return current company and location or '-'."""
        if obj.current_company:
            location = obj.current_company_location.name if obj.current_company_location else "No location"
            return f"{obj.current_company.name} ({location})"
        return "-"
    get_current_company.short_description = "Current Company (Client Workplace)"

    def get_past_companies(self, obj):
        """Return comma-separated list of past companies or '-'."""
        past_companies = [
            f"{co.organization.name} ({co.organization.industry.name})" if co.organization.industry else co.organization.name
            for co in obj.clientorganization_set.exclude(organization=obj.current_company)
        ]
        return ", ".join(past_companies) if past_companies else "-"
    get_past_companies.short_description = "Past Companies"


class OrganizationForm(forms.ModelForm):

    """Form for editing Organization in the admin."""

    class Meta:
        model = Organization
        fields = '__all__'
        labels = {
            'head_office': 'Head Office',
            'current_workplace': 'Current Workplace'
        }


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    """Admin for Organization."""

    form = OrganizationForm
    list_display = ('id', 'name', 'get_industry', 'head_office', 'created_at', 'updated_at')
    search_fields = ('name', 'industry__name', 'head_office__name', 'current_workplace__name')
    fields = ('name', 'industry', 'head_office')

    def get_industry(self, obj):
        """Return industry name or '-'."""
        return obj.industry.name if obj.industry else "-"
    get_industry.short_description = 'Industry'


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):

    """Admin for Industry."""

    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ['name']
    readonly_fields = ('created_at', 'updated_at')
    exclude = ['deleted_at']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):

    """Admin for Location."""

    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ['name']
    readonly_fields = ('created_at', 'updated_at')
    exclude = ['deleted_at']
