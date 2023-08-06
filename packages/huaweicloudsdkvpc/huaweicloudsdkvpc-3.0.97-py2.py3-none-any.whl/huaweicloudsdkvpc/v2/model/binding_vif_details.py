# coding: utf-8

import re
import six



from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class BindingVifDetails:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """

    sensitive_list = []

    openapi_types = {
        'primary_interface': 'bool'
    }

    attribute_map = {
        'primary_interface': 'primary_interface'
    }

    def __init__(self, primary_interface=None):
        """BindingVifDetails

        The model defined in huaweicloud sdk

        :param primary_interface: 功能说明：取值为true，表示是虚拟机的主网卡。
        :type primary_interface: bool
        """
        
        

        self._primary_interface = None
        self.discriminator = None

        if primary_interface is not None:
            self.primary_interface = primary_interface

    @property
    def primary_interface(self):
        """Gets the primary_interface of this BindingVifDetails.

        功能说明：取值为true，表示是虚拟机的主网卡。

        :return: The primary_interface of this BindingVifDetails.
        :rtype: bool
        """
        return self._primary_interface

    @primary_interface.setter
    def primary_interface(self, primary_interface):
        """Sets the primary_interface of this BindingVifDetails.

        功能说明：取值为true，表示是虚拟机的主网卡。

        :param primary_interface: The primary_interface of this BindingVifDetails.
        :type primary_interface: bool
        """
        self._primary_interface = primary_interface

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
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, BindingVifDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
