"""
Lcapy is a Python library for symbolic linear circuit and signal analysis.

Lcapy can analyse circuits described with netlists using modified nodal
analysis.  See lcapy.netlist

Alternatively, Lcapy can analyse networks and circuits formed by
combining one, two, and three port networks.  See lcapy.oneport

For detailed documentation see http://lcapy.readthedocs.io/en/latest

Copyright 2014--2022 Michael Hayes, UCECE
"""
from __future__ import absolute_import, print_function
del absolute_import, print_function

name = "lcapy"

import pkg_resources

__version__ = pkg_resources.require('lcapy')[0].version
lcapy_version = __version__

import sys
if sys.version_info[0] == 2 and sys.version_info[1] < 6:
    raise ImportError("Python Version 2.6 or above is required for Lcapy.")
else:  # Python 3
    pass
    # Here we can also check for specific Python 3 versions, if needed

del sys

from .functions import *
from .symbols import *
from .circuit import *
from .oneport import *
from .twoport import *
from .expr import *
from .voltage import voltage, noisevoltage, phasorvoltage
from .current import current, noisecurrent, phasorcurrent
from .admittance import admittance
from .impedance import impedance
from .transfer import transfer
from .resistance import resistance
from .conductance import conductance
from .capacitance import capacitance
from .inductance import inductance
from .reactance import reactance
from .susceptance import susceptance
from .printing import *
from .sym import *
from .matrix import *
from .smatrix import *
from .tmatrix import *
from .vector import *
from .statespace import *
from .dtstatespace import *
from .laplace import *
from .nettransform import *
from .randomnetwork import *
from .simulator import *
from .fexpr import fexpr
from .sexpr import sexpr, zp2tf, tf, pr2tf
from .texpr import texpr
from .cexpr import cexpr
from .omegaexpr import omegaexpr
from .normomegaexpr import Omegaexpr
from .normfexpr import Fexpr
from .phasor import phasor
from .discretetime import *
from .dltifilter import *
from .diffeq import *
from .dft import *
from .inverse_dft import *
from .state import state
# Do not import units.u since this will conflict with unit step
from .units import volts, amperes, ohms, siemens, watts

def show_version():
    """Show versions of Lcapy, SymPy, NumPy, MatplotLib, SciPy, and Python."""

    from sys import version as python_version
    from sympy import __version__ as sympy_version
    from numpy import __version__ as numpy_version
    from scipy import __version__ as scipy_version
    from matplotlib import __version__ as matplotlib_version

    print('Python: %s\nSymPy: %s\nNumPy: %s\nMatplotlib: %s\nSciPy: %s\nLcapy: %s' %
          (python_version, sympy_version, numpy_version,
           matplotlib_version, scipy_version, lcapy_version))

# The following is to help sympify deal with j.
# A better fix might be to define an Lcapy class for j and to
# use the __sympy_ method.
from sympy.core.sympify import converter
from sympy import Symbol
converter['j'] = j
converter[Symbol('j')] = j
