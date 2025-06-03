from unittest import TestCase

from .models import Client, Company


class ClientModelTest(TestCase):
    def test_create_client(self):

        # First create a company (no need to specify the ID)
        company = Company.objects.create(
            name="Client Company"
        )

        # Now create a Client with a unique email (ensure it's different each time)
        client = Client.objects.create(
            name="Client Name",
            email="client1@email.test",  # Make sure the email is unique
            phone="1122334455"
        )

        # Assign the Company to the Client using the set method
        client.companies.set([company])

        # Check that the Client name is correctly assigned
        self.assertEqual(client.name, "Client Name")

        # Check that the Client has the right Company
        self.assertIn(company, client.companies.all())

        # Optionally, test that the Client's email is correctly assigned
        self.assertEqual(client.email, "client1@email.test")
