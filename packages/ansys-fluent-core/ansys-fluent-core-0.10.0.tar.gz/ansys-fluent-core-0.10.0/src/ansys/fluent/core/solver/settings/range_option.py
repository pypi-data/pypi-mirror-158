#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from .option import option
from .auto_range_on import auto_range_on
from .auto_range_off import auto_range_off
class range_option(Group):
    """
    'range_option' child.
    """

    fluent_name = "range-option"

    child_names = \
        ['option', 'auto_range_on', 'auto_range_off']

    option: option = option
    """
    option child of range_option.
    """
    auto_range_on: auto_range_on = auto_range_on
    """
    auto_range_on child of range_option.
    """
    auto_range_off: auto_range_off = auto_range_off
    """
    auto_range_off child of range_option.
    """
