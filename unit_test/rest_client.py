from unittest import TestCase
from mock import patch
from requests import Session

from external_ingestor.client.RestApiClient import RestApiClient
from external_ingestor.utils.uri_builder import UriBuilder


class RestApiClientTest(TestCase):
    def setUp(self):
        self.target_domain = "http://kitabisa.com"
        self.header =  {
          'APIKey': 'abcde'
        }
        self.authentication = "vianhazman@gmail.com", 1234
        self.max_retry = 3
        self.client = RestApiClient(self.target_domain, self.authentication, self.header, self.max_retry)

    def test_get_class_name(self):
        actual_class_name = self.client.get_class_name()
        expected_class_name = "RestApiClient"
        self.assertEqual(actual_class_name, expected_class_name)

    def test_get_authentication(self):
        actual_authentication = self.client.get_auth()
        expected_authentication = self.authentication
        self.assertEqual(actual_authentication, expected_authentication)

    def test_get_target_domain(self):
        actual_target_domain = self.client.get_target_domain()
        self.assertEqual(actual_target_domain, self.target_domain)

    def test_get_header(self):
        actual_header = self.client.get_header()
        expected_header = {
            'APIKey': 'abcde',
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        self.assertEqual(actual_header, expected_header)

    def test_get_max_retry(self):
        actual_max_retry = self.client.get_max_retry()
        self.assertEqual(actual_max_retry, self.max_retry)

    @patch.object(UriBuilder, "get_full_path", return_value = "kitabisa.com/v1/?data1=abcd&data2=efgh")
    def test_generate_endpoint_if_args_exist(self, mock_uri_builder):
        path = "/v1/"
        args = {"data1": "abcd", "data2": "efgh"}
        actual_data = self.client.generate_endpoint(path, args)
        self.assertTrue(mock_uri_builder.called)
        self.assertEqual(actual_data, "kitabisa.com/v1/?data1=abcd&data2=efgh")

    @patch.object(Session, 'get')
    def test_request_get(self, mock_request):
        # test if requests.get was called
        # with the given url or not
        args = {"data1": "abcd", "data2": "efgh"}
        path = "/v1/"
        expected_header = {
            'APIKey': 'abcde',
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        self.client.__get__(path,args)
        mock_request.assert_called_once_with("http://kitabisa.com/v1/?data1=abcd&data2=efgh", headers= expected_header)