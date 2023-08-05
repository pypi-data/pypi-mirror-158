#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from .pre_sweeps import pre_sweeps
from .post_sweeps import post_sweeps
from .max_cycle import max_cycle
class fixed_cycle_parameters(Group):
    """
    'fixed_cycle_parameters' child.
    """

    fluent_name = "fixed-cycle-parameters"

    child_names = \
        ['pre_sweeps', 'post_sweeps', 'max_cycle']

    pre_sweeps: pre_sweeps = pre_sweeps
    """
    pre_sweeps child of fixed_cycle_parameters.
    """
    post_sweeps: post_sweeps = post_sweeps
    """
    post_sweeps child of fixed_cycle_parameters.
    """
    max_cycle: max_cycle = max_cycle
    """
    max_cycle child of fixed_cycle_parameters.
    """
