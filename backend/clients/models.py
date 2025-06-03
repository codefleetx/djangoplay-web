from django.db import models

INDUSTRY_CHOICES = (
    ('aerospace', 'Aerospace'),
    ('agriculture', 'Agriculture'),
    ('automotive', 'Automotive'),
    ('banking', 'Banking'),
    ('biotechnology', 'Biotechnology'),
    ('chemicals', 'Chemicals'),
    ('construction', 'Construction'),
    ('consumer_goods', 'Consumer Goods'),
    ('education', 'Education'),
    ('energy', 'Energy'),
    ('entertainment', 'Entertainment'),
    ('finance', 'Finance'),
    ('food_beverage', 'Food & Beverage'),
    ('healthcare', 'Healthcare'),
    ('hospitality', 'Hospitality'),
    ('information_technology', 'Information Technology'),
    ('insurance', 'Insurance'),
    ('logistics', 'Logistics'),
    ('manufacturing', 'Manufacturing'),
    ('media', 'Media'),
    ('mining', 'Mining'),
    ('pharmaceuticals', 'Pharmaceuticals'),
    ('real_estate', 'Real Estate'),
    ('retail', 'Retail'),
    ('telecommunications', 'Telecommunications'),
    ('transportation', 'Transportation'),
    ('utilities', 'Utilities'),
)


class Company(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit ID
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Client(models.Model):
    id = models.AutoField(primary_key=True)  # Explicit ID
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True)  # Changed to CharField
    companies = models.ManyToManyField(Company, blank=True)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
