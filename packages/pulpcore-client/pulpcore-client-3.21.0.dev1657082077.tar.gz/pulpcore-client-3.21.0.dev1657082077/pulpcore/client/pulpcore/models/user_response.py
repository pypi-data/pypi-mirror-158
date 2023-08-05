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

from pulpcore.client.pulpcore.configuration import Configuration


class UserResponse(object):
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
        'pulp_href': 'str',
        'id': 'int',
        'username': 'str',
        'first_name': 'str',
        'last_name': 'str',
        'email': 'str',
        'is_staff': 'bool',
        'is_active': 'bool',
        'date_joined': 'datetime',
        'groups': 'list[UserGroupResponse]'
    }

    attribute_map = {
        'pulp_href': 'pulp_href',
        'id': 'id',
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
        'is_staff': 'is_staff',
        'is_active': 'is_active',
        'date_joined': 'date_joined',
        'groups': 'groups'
    }

    def __init__(self, pulp_href=None, id=None, username=None, first_name=None, last_name=None, email=None, is_staff=False, is_active=True, date_joined=None, groups=None, local_vars_configuration=None):  # noqa: E501
        """UserResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._pulp_href = None
        self._id = None
        self._username = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._is_staff = None
        self._is_active = None
        self._date_joined = None
        self._groups = None
        self.discriminator = None

        if pulp_href is not None:
            self.pulp_href = pulp_href
        if id is not None:
            self.id = id
        self.username = username
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email
        if is_staff is not None:
            self.is_staff = is_staff
        if is_active is not None:
            self.is_active = is_active
        if date_joined is not None:
            self.date_joined = date_joined
        if groups is not None:
            self.groups = groups

    @property
    def pulp_href(self):
        """Gets the pulp_href of this UserResponse.  # noqa: E501


        :return: The pulp_href of this UserResponse.  # noqa: E501
        :rtype: str
        """
        return self._pulp_href

    @pulp_href.setter
    def pulp_href(self, pulp_href):
        """Sets the pulp_href of this UserResponse.


        :param pulp_href: The pulp_href of this UserResponse.  # noqa: E501
        :type: str
        """

        self._pulp_href = pulp_href

    @property
    def id(self):
        """Gets the id of this UserResponse.  # noqa: E501


        :return: The id of this UserResponse.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UserResponse.


        :param id: The id of this UserResponse.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def username(self):
        """Gets the username of this UserResponse.  # noqa: E501

        Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.  # noqa: E501

        :return: The username of this UserResponse.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this UserResponse.

        Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.  # noqa: E501

        :param username: The username of this UserResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and username is None:  # noqa: E501
            raise ValueError("Invalid value for `username`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                username is not None and len(username) > 150):
            raise ValueError("Invalid value for `username`, length must be less than or equal to `150`")  # noqa: E501

        self._username = username

    @property
    def first_name(self):
        """Gets the first_name of this UserResponse.  # noqa: E501

        First name  # noqa: E501

        :return: The first_name of this UserResponse.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this UserResponse.

        First name  # noqa: E501

        :param first_name: The first_name of this UserResponse.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                first_name is not None and len(first_name) > 150):
            raise ValueError("Invalid value for `first_name`, length must be less than or equal to `150`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this UserResponse.  # noqa: E501

        Last name  # noqa: E501

        :return: The last_name of this UserResponse.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this UserResponse.

        Last name  # noqa: E501

        :param last_name: The last_name of this UserResponse.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                last_name is not None and len(last_name) > 150):
            raise ValueError("Invalid value for `last_name`, length must be less than or equal to `150`")  # noqa: E501

        self._last_name = last_name

    @property
    def email(self):
        """Gets the email of this UserResponse.  # noqa: E501

        Email address  # noqa: E501

        :return: The email of this UserResponse.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserResponse.

        Email address  # noqa: E501

        :param email: The email of this UserResponse.  # noqa: E501
        :type: str
        """

        self._email = email

    @property
    def is_staff(self):
        """Gets the is_staff of this UserResponse.  # noqa: E501

        Designates whether the user can log into this admin site.  # noqa: E501

        :return: The is_staff of this UserResponse.  # noqa: E501
        :rtype: bool
        """
        return self._is_staff

    @is_staff.setter
    def is_staff(self, is_staff):
        """Sets the is_staff of this UserResponse.

        Designates whether the user can log into this admin site.  # noqa: E501

        :param is_staff: The is_staff of this UserResponse.  # noqa: E501
        :type: bool
        """

        self._is_staff = is_staff

    @property
    def is_active(self):
        """Gets the is_active of this UserResponse.  # noqa: E501

        Designates whether this user should be treated as active.  # noqa: E501

        :return: The is_active of this UserResponse.  # noqa: E501
        :rtype: bool
        """
        return self._is_active

    @is_active.setter
    def is_active(self, is_active):
        """Sets the is_active of this UserResponse.

        Designates whether this user should be treated as active.  # noqa: E501

        :param is_active: The is_active of this UserResponse.  # noqa: E501
        :type: bool
        """

        self._is_active = is_active

    @property
    def date_joined(self):
        """Gets the date_joined of this UserResponse.  # noqa: E501

        Date joined  # noqa: E501

        :return: The date_joined of this UserResponse.  # noqa: E501
        :rtype: datetime
        """
        return self._date_joined

    @date_joined.setter
    def date_joined(self, date_joined):
        """Sets the date_joined of this UserResponse.

        Date joined  # noqa: E501

        :param date_joined: The date_joined of this UserResponse.  # noqa: E501
        :type: datetime
        """

        self._date_joined = date_joined

    @property
    def groups(self):
        """Gets the groups of this UserResponse.  # noqa: E501


        :return: The groups of this UserResponse.  # noqa: E501
        :rtype: list[UserGroupResponse]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """Sets the groups of this UserResponse.


        :param groups: The groups of this UserResponse.  # noqa: E501
        :type: list[UserGroupResponse]
        """

        self._groups = groups

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
        if not isinstance(other, UserResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserResponse):
            return True

        return self.to_dict() != other.to_dict()
