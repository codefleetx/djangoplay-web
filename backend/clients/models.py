from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):

    """Abstract base model with timestamp and soft delete fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark instance as deleted with timestamp."""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore soft-deleted instance."""
        self.deleted_at = None
        self.save()


class ActiveManager(models.Manager):

    """Manager to filter out soft-deleted records."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class Industry(TimeStampedModel):

    """Model for an industry."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = "Industry"
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name


class Location(TimeStampedModel):

    """Model for a location."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name


class Organization(TimeStampedModel):

    """Model for an organization."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    head_office = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='org_head_office')
    current_workplace = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='org_current_workplace')

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = "Organization"
        verbose_name_plural = "Organization Dashboard"

    def __str__(self):
        return self.name


class ClientOrganization(models.Model):

    """Model for client-organization association."""

    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    previous_workplace = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Previous Business Affiliation"
        verbose_name_plural = "Previous Business Affiliations"
        unique_together = ('client', 'organization', 'from_date')

    def __str__(self):
        return f"{self.client.name} - {self.organization.name}"


class Client(TimeStampedModel):

    """Model for a client."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    current_company = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='client_current_company'
    )
    current_company_location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    current_company_joining_day = models.DateField(null=True, blank=True)
    past_companies = models.ManyToManyField(
        Organization,
        through='ClientOrganization',
        related_name='client_past_companies',
        blank=True
    )
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)

    objects = ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = "Client"
        verbose_name_plural = "Client Dashboard"

    def __str__(self):
        return self.name
