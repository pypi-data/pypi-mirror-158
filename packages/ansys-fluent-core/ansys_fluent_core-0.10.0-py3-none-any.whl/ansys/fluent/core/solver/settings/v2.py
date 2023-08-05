#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from .option import option
from .constant import constant
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class v2(Group):
    """
    'v2' child.
    """

    fluent_name = "v2"

    child_names = \
        ['option', 'constant', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of v2.
    """
    constant: constant = constant
    """
    constant child of v2.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of v2.
    """
    field_name: field_name = field_name
    """
    field_name child of v2.
    """
    udf: udf = udf
    """
    udf child of v2.
    """
