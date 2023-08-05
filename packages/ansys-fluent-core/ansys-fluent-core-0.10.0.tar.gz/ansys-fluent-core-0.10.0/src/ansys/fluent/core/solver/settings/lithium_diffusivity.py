#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from .option import option
from .constant import constant
from .boussinesq import boussinesq
from .coefficients import coefficients
from .number_of_coefficients import number_of_coefficients
from .piecewise_polynomial import piecewise_polynomial
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .piecewise_linear import piecewise_linear
from .anisotropic import anisotropic
from .orthotropic import orthotropic
from .var_class import var_class
class lithium_diffusivity(Group):
    """
    'lithium_diffusivity' child.
    """

    fluent_name = "lithium-diffusivity"

    child_names = \
        ['option', 'constant', 'boussinesq', 'coefficients',
         'number_of_coefficients', 'piecewise_polynomial',
         'nasa_9_piecewise_polynomial', 'piecewise_linear', 'anisotropic',
         'orthotropic', 'var_class']

    option: option = option
    """
    option child of lithium_diffusivity.
    """
    constant: constant = constant
    """
    constant child of lithium_diffusivity.
    """
    boussinesq: boussinesq = boussinesq
    """
    boussinesq child of lithium_diffusivity.
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of lithium_diffusivity.
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of lithium_diffusivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of lithium_diffusivity.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of lithium_diffusivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of lithium_diffusivity.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of lithium_diffusivity.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of lithium_diffusivity.
    """
    var_class: var_class = var_class
    """
    var_class child of lithium_diffusivity.
    """
