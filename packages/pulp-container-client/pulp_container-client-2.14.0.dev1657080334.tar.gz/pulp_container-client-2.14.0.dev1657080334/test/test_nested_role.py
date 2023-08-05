# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_container
from pulpcore.client.pulp_container.models.nested_role import NestedRole  # noqa: E501
from pulpcore.client.pulp_container.rest import ApiException

class TestNestedRole(unittest.TestCase):
    """NestedRole unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test NestedRole
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_container.models.nested_role.NestedRole()  # noqa: E501
        if include_optional :
            return NestedRole(
                users = [
                    '0'
                    ], 
                groups = [
                    '0'
                    ], 
                role = '0'
            )
        else :
            return NestedRole(
                role = '0',
        )

    def testNestedRole(self):
        """Test NestedRole"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
