# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.catalog import Catalog  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.test import BaseTestCase


class TestCatalogController(BaseTestCase):
    """CatalogController integration test stubs"""

    def test_catalog_get(self):
        """Test case for catalog_get

        get the catalog of services that the service broker offers
        """
        headers = [('X_Broker_API_Version', 'X_Broker_API_Version_example'),
                   ('X_Broker_API_Originating_Identity', 'X_Broker_API_Originating_Identity_example'),
                   ('X_Broker_API_Request_Identity', 'X_Broker_API_Request_Identity_example')]
        response = self.client.open(
            '/v2/catalog',
            method='GET',
            headers=headers,
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
