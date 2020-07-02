from unittest import TestCase

from requests import Session
from mock import patch

from external_ingestor.client.ZendeskClient import ZendeskClient


class RestApiClientTest(TestCase):
    def setUp(self):
        self.settings = {
            "email" : "vianhazman@gmail.com",
            "password" : "passwordrahasia"
        }
        self.target_domain = "https://vianhazman.zendesk.com"
        self.target_path = "/api/v2/incremental/tickets.json"
        self.client = ZendeskClient(self.target_domain, self.settings)

    def test_get_authentication(self):
        actual_authentication = self.client.get_auth()
        expected_authentication = "{}/token".format(self.settings['email']), self.settings['password']
        self.assertEqual(actual_authentication, expected_authentication)

    @patch.object(ZendeskClient, 'get_ticket_incremental')
    def test_request(self, mock_request):
        epoch_time = 1591013586
        self.client.get_ticket_incremental(self.target_path, epoch_time)
        mock_request.assert_called_once_with(self.target_path, epoch_time)
