from django.test import TestCase

from .models import Client, ClientOrganization, Industry, Location, Organization


class IndustryModelTest(TestCase):

    def setUp(self):
        # Ensure unique creation of the Industry object
        self.industry, _ = Industry.objects.get_or_create(name="Technology")

    def test_industry_creation(self):
        """Test if Industry object is created correctly."""
        self.assertEqual(self.industry.name, "Technology")
        self.assertIsNotNone(self.industry.created_at)
        self.assertIsNone(self.industry.deleted_at)

    def test_industry_str(self):
        """Test the string representation of Industry."""
        self.assertEqual(str(self.industry), "Technology")


class LocationModelTest(TestCase):

    def setUp(self):
        # Ensure unique creation of the Location object
        self.location, _ = Location.objects.get_or_create(name="Kolhapur")

    def test_location_creation(self):
        """Test if Location object is created correctly."""
        self.assertEqual(self.location.name, "Kolhapur")
        self.assertIsNotNone(self.location.created_at)
        self.assertIsNone(self.location.deleted_at)

    def test_location_str(self):
        """Test the string representation of Location."""
        self.assertEqual(str(self.location), "Kolhapur")


class OrganizationModelTest(TestCase):

    def setUp(self):
        # Ensure unique creation of related Industry and Location objects
        self.industry, _ = Industry.objects.get_or_create(name="Finance")
        self.location, _ = Location.objects.get_or_create(name="Pune")
        self.organization, _ = Organization.objects.get_or_create(
            name="Tech Corp",
            industry=self.industry,
            head_office=self.location
        )

    def test_organization_creation(self):
        """Test if Organization object is created correctly."""
        self.assertEqual(self.organization.name, "Tech Corp")
        self.assertEqual(self.organization.industry.name, "Finance")
        self.assertEqual(self.organization.head_office.name, "Pune")
        self.assertIsNotNone(self.organization.created_at)
        self.assertIsNone(self.organization.deleted_at)

    def test_organization_str(self):
        """Test the string representation of Organization."""
        self.assertEqual(str(self.organization), "Tech Corp")


class ClientModelTest(TestCase):

    def setUp(self):
        # Ensure unique creation of related Industry, Location, and Organization objects
        self.industry, _ = Industry.objects.get_or_create(name="Healthcare")
        self.location, _ = Location.objects.get_or_create(name="Mumbai")
        self.organization, _ = Organization.objects.get_or_create(
            name="Health Corp",
            industry=self.industry,
            head_office=self.location
        )
        self.client, _ = Client.objects.get_or_create(
            name="Shekhar Bhosale",
            email="shekhar@paystream.com",
            current_company=self.organization,
            current_company_location=self.location
        )

    def test_client_creation(self):
        """Test if Client object is created correctly."""
        self.assertEqual(self.client.name, "Shekhar Bhosale")
        self.assertEqual(self.client.email, "shekhar@paystream.com")
        self.assertEqual(self.client.current_company.name, "Health Corp")
        self.assertIsNotNone(self.client.created_at)
        self.assertIsNone(self.client.deleted_at)

    def test_client_str(self):
        """Test the string representation of Client."""
        self.assertEqual(str(self.client), "Shekhar Bhosale")


class ClientOrganizationModelTest(TestCase):

    def setUp(self):
        self.client, _ = Client.objects.get_or_create(name="Shekhar Bhosale", email="shekhar@paystream.com")
        self.organization, _ = Organization.objects.get_or_create(name="Tech Inc.")
        self.client_org, _ = ClientOrganization.objects.get_or_create(
            client=self.client,
            organization=self.organization,
            from_date="2021-01-01",
            to_date="2022-01-01"
        )

    def test_client_organization_creation(self):
        """Test if ClientOrganization object is created correctly."""
        self.assertEqual(self.client_org.client.name, "Shekhar Bhosale")
        self.assertEqual(self.client_org.organization.name, "Tech Inc.")
        self.assertEqual(self.client_org.from_date, "2021-01-01")
        self.assertEqual(self.client_org.to_date, "2022-01-01")

    def test_client_organization_str(self):
        """Test the string representation of ClientOrganization."""
        self.assertEqual(str(self.client_org), "Shekhar Bhosale - Tech Inc.")


class SoftDeleteTest(TestCase):

    def setUp(self):
        # Ensure unique creation of related Industry and Location objects
        self.industry, _ = Industry.objects.get_or_create(name="Retail")
        self.location, _ = Location.objects.get_or_create(name="Tokyo")
        self.organization, _ = Organization.objects.get_or_create(
            name="Retail Corp",
            industry=self.industry,
            head_office=self.location
        )

    def test_soft_delete(self):
        """Test if soft delete works correctly."""
        self.organization.soft_delete()
        self.organization.refresh_from_db()
        self.assertIsNotNone(self.organization.deleted_at)

    def test_restore(self):
        """Test if restore works correctly."""
        self.organization.soft_delete()
        self.organization.restore()
        self.organization.refresh_from_db()
        self.assertIsNone(self.organization.deleted_at)


class ActiveManagerTest(TestCase):

    def setUp(self):
        # Ensure unique creation of related Industry and Location objects
        self.industry, _ = Industry.objects.get_or_create(name="Tech")
        self.location, _ = Location.objects.get_or_create(name="Osaka")
        self.active_org, _ = Organization.objects.get_or_create(
            name="Active Org",
            industry=self.industry,
            head_office=self.location
        )
        self.deleted_org, _ = Organization.objects.get_or_create(
            name="Deleted Org",
            industry=self.industry,
            head_office=self.location
        )
        self.deleted_org.soft_delete()

    def test_active_manager(self):
        """Test if ActiveManager filters out soft-deleted records."""
        active_organizations = Organization.objects.all()
        self.assertIn(self.active_org, active_organizations)
        self.assertNotIn(self.deleted_org, active_organizations)
