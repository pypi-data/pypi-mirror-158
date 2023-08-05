# coding: utf-8

"""
    Pulp 3 API

    Fetch, Upload, Organize, and Distribute Software Packages  # noqa: E501

    The version of the OpenAPI document: v3
    Contact: pulp-list@redhat.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from pulpcore.client.pulp_container.configuration import Configuration


class PatchedcontainerContainerPushRepository(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'manifest_signing_service': 'str',
        'pulp_labels': 'object',
        'name': 'str',
        'retain_repo_versions': 'int',
        'description': 'str'
    }

    attribute_map = {
        'manifest_signing_service': 'manifest_signing_service',
        'pulp_labels': 'pulp_labels',
        'name': 'name',
        'retain_repo_versions': 'retain_repo_versions',
        'description': 'description'
    }

    def __init__(self, manifest_signing_service=None, pulp_labels=None, name=None, retain_repo_versions=None, description=None, local_vars_configuration=None):  # noqa: E501
        """PatchedcontainerContainerPushRepository - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._manifest_signing_service = None
        self._pulp_labels = None
        self._name = None
        self._retain_repo_versions = None
        self._description = None
        self.discriminator = None

        self.manifest_signing_service = manifest_signing_service
        if pulp_labels is not None:
            self.pulp_labels = pulp_labels
        if name is not None:
            self.name = name
        self.retain_repo_versions = retain_repo_versions
        self.description = description

    @property
    def manifest_signing_service(self):
        """Gets the manifest_signing_service of this PatchedcontainerContainerPushRepository.  # noqa: E501

        A reference to an associated signing service.  # noqa: E501

        :return: The manifest_signing_service of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :rtype: str
        """
        return self._manifest_signing_service

    @manifest_signing_service.setter
    def manifest_signing_service(self, manifest_signing_service):
        """Sets the manifest_signing_service of this PatchedcontainerContainerPushRepository.

        A reference to an associated signing service.  # noqa: E501

        :param manifest_signing_service: The manifest_signing_service of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :type: str
        """

        self._manifest_signing_service = manifest_signing_service

    @property
    def pulp_labels(self):
        """Gets the pulp_labels of this PatchedcontainerContainerPushRepository.  # noqa: E501


        :return: The pulp_labels of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :rtype: object
        """
        return self._pulp_labels

    @pulp_labels.setter
    def pulp_labels(self, pulp_labels):
        """Sets the pulp_labels of this PatchedcontainerContainerPushRepository.


        :param pulp_labels: The pulp_labels of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :type: object
        """

        self._pulp_labels = pulp_labels

    @property
    def name(self):
        """Gets the name of this PatchedcontainerContainerPushRepository.  # noqa: E501

        A unique name for this repository.  # noqa: E501

        :return: The name of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PatchedcontainerContainerPushRepository.

        A unique name for this repository.  # noqa: E501

        :param name: The name of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def retain_repo_versions(self):
        """Gets the retain_repo_versions of this PatchedcontainerContainerPushRepository.  # noqa: E501

        Retain X versions of the repository. Default is null which retains all versions. This is provided as a tech preview in Pulp 3 and may change in the future.  # noqa: E501

        :return: The retain_repo_versions of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :rtype: int
        """
        return self._retain_repo_versions

    @retain_repo_versions.setter
    def retain_repo_versions(self, retain_repo_versions):
        """Sets the retain_repo_versions of this PatchedcontainerContainerPushRepository.

        Retain X versions of the repository. Default is null which retains all versions. This is provided as a tech preview in Pulp 3 and may change in the future.  # noqa: E501

        :param retain_repo_versions: The retain_repo_versions of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :type: int
        """
        if (self.local_vars_configuration.client_side_validation and
                retain_repo_versions is not None and retain_repo_versions < 1):  # noqa: E501
            raise ValueError("Invalid value for `retain_repo_versions`, must be a value greater than or equal to `1`")  # noqa: E501

        self._retain_repo_versions = retain_repo_versions

    @property
    def description(self):
        """Gets the description of this PatchedcontainerContainerPushRepository.  # noqa: E501

        An optional description.  # noqa: E501

        :return: The description of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this PatchedcontainerContainerPushRepository.

        An optional description.  # noqa: E501

        :param description: The description of this PatchedcontainerContainerPushRepository.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                description is not None and len(description) < 1):
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `1`")  # noqa: E501

        self._description = description

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PatchedcontainerContainerPushRepository):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, PatchedcontainerContainerPushRepository):
            return True

        return self.to_dict() != other.to_dict()
