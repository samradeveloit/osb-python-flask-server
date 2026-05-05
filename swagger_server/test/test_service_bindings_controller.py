# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.async_operation import AsyncOperation  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.last_operation_resource import LastOperationResource  # noqa: E501
from swagger_server.models.service_binding_request import ServiceBindingRequest  # noqa: E501
from swagger_server.models.service_binding_resource import ServiceBindingResource  # noqa: E501
from swagger_server.models.service_binding_response import ServiceBindingResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestServiceBindingsController(BaseTestCase):
    """ServiceBindingsController integration test stubs"""

    def test_service_binding_binding(self):
        """Test case for service_binding_binding

        generation of a service binding
        """
        body = ServiceBindingRequest()
        query_string = [('accepts_incomplete', true)]
        headers = [('X_Broker_API_Version', 'X_Broker_API_Version_example'),
                   ('X_Broker_API_Originating_Identity', 'X_Broker_API_Originating_Identity_example'),
                   ('X_Broker_API_Request_Identity', 'X_Broker_API_Request_Identity_example')]
        response = self.client.open(
            '/v2/service_instances/**/service_bindings/{binding_id}'.format(binding_id='binding_id_example'),
            method='PUT',
            data=json.dumps(body),
            headers=headers,
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_service_binding_get(self):
        """Test case for service_binding_get

        gets a service binding
        """
        query_string = [('service_id', 'service_id_example'),
                        ('plan_id', 'plan_id_example')]
        headers = [('X_Broker_API_Version', 'X_Broker_API_Version_example'),
                   ('X_Broker_API_Originating_Identity', 'X_Broker_API_Originating_Identity_example'),
                   ('X_Broker_API_Request_Identity', 'X_Broker_API_Request_Identity_example')]
        response = self.client.open(
            '/v2/service_instances/**/service_bindings/{binding_id}'.format(binding_id='binding_id_example'),
            method='GET',
            headers=headers,
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_service_binding_last_operation_get(self):
        """Test case for service_binding_last_operation_get

        last requested operation state for service binding
        """
        query_string = [('service_id', 'service_id_example'),
                        ('plan_id', 'plan_id_example'),
                        ('operation', 'operation_example')]
        headers = [('X_Broker_API_Version', 'X_Broker_API_Version_example'),
                   ('X_Broker_API_Originating_Identity', 'X_Broker_API_Originating_Identity_example'),
                   ('X_Broker_API_Request_Identity', 'X_Broker_API_Request_Identity_example')]
        response = self.client.open(
            '/v2/service_instances/**/service_bindings/{binding_id}/last_operation'.format(binding_id='binding_id_example'),
            method='GET',
            headers=headers,
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_service_binding_unbinding(self):
        """Test case for service_binding_unbinding

        deprovision of a service binding
        """
        query_string = [('service_id', 'service_id_example'),
                        ('plan_id', 'plan_id_example'),
                        ('accepts_incomplete', true)]
        headers = [('X_Broker_API_Version', 'X_Broker_API_Version_example'),
                   ('X_Broker_API_Originating_Identity', 'X_Broker_API_Originating_Identity_example'),
                   ('X_Broker_API_Request_Identity', 'X_Broker_API_Request_Identity_example')]
        response = self.client.open(
            '/v2/service_instances/**/service_bindings/{binding_id}'.format(binding_id='binding_id_example'),
            method='DELETE',
            headers=headers,
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
