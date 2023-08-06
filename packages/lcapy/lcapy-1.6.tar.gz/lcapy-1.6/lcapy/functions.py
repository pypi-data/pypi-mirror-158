"""This module wraps SymPy functions and provides a few others.
The underlying SymPy function is obtained with the sympy attribute.

Copyright 2014--2022 Michael Hayes, UCECE
"""

from .units import u as uu
import sympy as sym

__all__ = ('conjugate', 'sqrt', 'exp', 'log', 'log10', 'sin', 'cos',
           'tan', 'cot', 'asin', 'acos', 'atan', 'atan2', 'acot',
           'sinh', 'cosh', 'tanh', 'coth', 'asinh', 'acosh', 'atanh',
           'acoth', 'gcd', 'sign', 'diff', 'integrate', 'u', 'H',
           'heaviside', 'Heaviside', 'delta', 'DiracDelta', 'ui',
           'us', 'unitimpulse', 'unitstep', 'UnitImpulse', 'UnitStep',
           'rect', 'sinc', 'sincn', 'sincu', 'psinc', 'tri', 'trap',
           'ramp', 'rampstep', 'Sum', 'dtrect', 'dtsign', 'Piecewise',
           'Eq', 'Ne', 'Lt', 'Le', 'Gt', 'Ge', 'Derivative',
           'Integral', 'Max', 'Min', 're', 'im', 'MatMul', 'MatAdd',
           'degrees', 'radians', 'limit')

from .extrafunctions import Degrees as Degrees1
from .extrafunctions import Radians as Radians1
from .extrafunctions import UnitImpulse as UnitImpulse1
from .extrafunctions import UnitStep as UnitStep1
from .extrafunctions import sincn as sincn1
from .extrafunctions import sincu as sincu1
from .extrafunctions import psinc as psinc1
from .extrafunctions import rect as rect1
from .extrafunctions import dtrect as dtrect1
from .extrafunctions import dtsign as dtsign1
from .extrafunctions import tri as tri1
from .extrafunctions import trap as trap1
from .extrafunctions import ramp as ramp1
from .extrafunctions import rampstep as rampstep1


class Function(object):

    def __init__(self, arg):

        if isinstance(arg, str):
            # Handled AppliedUndef
            arg = sym.Function(arg)
        self.expr = arg

    @property
    def sympy(self):
        """Return SymPy expression."""

        return self.expr

    def __call__(self, *args, **kwargs):

        func = self.expr

        e_args = list(map(expr, args))

        if func == sym.Piecewise:
            cls = e_args[0][0].__class__
        elif func in (sym.Integral, sym.integrate):
            # Integral(const, (tau, 0, t)) -> use t class
            # Integral(integrand, (tau, a, b)) -> use integrand class
            if e_args[0].is_constant:
                cls = e_args[1][2].__class__
            else:
                cls = e_args[0].__class__
        else:
            cls = e_args[0].__class__

            # Handle cases like atan2(1, omega)
            if len(e_args) > 1:
                if e_args[0].is_constant:
                    cls = e_args[1].__class__

        try:
            if cls.is_discrete_time_domain or cls.is_discrete_fourier_domain:

                # TODO: fix for Heaviside change
                for old, new in function_mapping.items():
                    if func is old:
                        func = new
                        break
        except:
            pass

        result = func(*delcapify(e_args), **kwargs)

        result = cls(result)

        if (self.expr in (sym.sin, sym.cos, sym.tan, sym.cot, sym.exp,
                          sym.sinh, sym.cosh, sym.tanh, sym.coth)
                and e_args[0].is_phase):
            result.part = ''
        elif self.expr in (sym.atan, sym.atan2):
            result.units = uu.rad
        elif self.expr == sym.diff and isinstance(e_args[1], Expr):
            result.units = e_args[0].units / e_args[1].units
        elif self.expr == Degrees1:
            result.units = uu.deg
        elif self.expr == Radians1:
            result.units = uu.rad
        elif self.expr == sym.integrate:
            if isinstance(e_args[1], Expr):
                result.units = e_args[0].units * e_args[1].units
            elif isinstance(e_args[1], tuple) and isinstance(e_args[1][0], Expr):
                result.units = e_args[0].units * e_args[1][0].units
        elif self.expr is sym.DiracDelta and isinstance(e_args[0], Expr):
            result.units = 1 / e_args[0].units

        return result

    def pdb(self):
        import pdb
        pdb.set_trace()
        return self


class Log10(Function):

    # TODO, figure out how to print as log10(x) rather than
    # the expansion log(x) / log(10).  This will require
    # deferment of the expansion.

    def __call__(self, arg):
        return super(Log10, self).__call__(arg, 10)


class SincnFunction(Function):
    """Normalized sinc function :math:`\sin(\pi x)/(\pi x)`."""


class SincuFunction(Function):
    """Unnormalized sinc function :math:`\sin(x)/(x)`."""


class PsincFunction(Function):
    """Periodic sinc function :math:`\sin(M * x)/(M * sin(x))`."""


conjugate = Function(sym.conjugate)

sqrt = Function(sym.sqrt)

exp = Function(sym.exp)

log = Function(sym.log)

log10 = Log10(sym.log)

sin = Function(sym.sin)

cos = Function(sym.cos)

tan = Function(sym.tan)

cot = Function(sym.cot)

asin = Function(sym.asin)

acos = Function(sym.acos)

atan = Function(sym.atan)

atan2 = Function(sym.atan2)

acot = Function(sym.acot)

sinh = Function(sym.sinh)

cosh = Function(sym.cosh)

tanh = Function(sym.tanh)

coth = Function(sym.coth)

asinh = Function(sym.asinh)

acosh = Function(sym.acosh)

atanh = Function(sym.atanh)

acoth = Function(sym.acoth)

gcd = Function(sym.gcd)

sign = Function(sym.sign)

degrees = Function(Degrees1)

radians = Function(Radians1)

diff = Function(sym.diff)

integrate = Function(sym.integrate)

limit = Function(sym.limit)

u = H = heaviside = Heaviside = Function(sym.Heaviside)

delta = DiracDelta = Function(sym.DiracDelta)

Piecewise = Function(sym.Piecewise)

Derivative = Function(sym.Derivative)

Integral = Function(sym.Integral)

Eq = Function(sym.Eq)

Ne = Function(sym.Ne)

Lt = Function(sym.Lt)

Le = Function(sym.Le)

Gt = Function(sym.Gt)

Ge = Function(sym.Ge)

Add = Function(sym.Add)

Mul = Function(sym.Mul)

MatAdd = Function(sym.MatAdd)

MatMul = Function(sym.MatMul)

Sum = Function(sym.Sum)

Min = Function(sym.Min)

Max = Function(sym.Max)

re = Function(sym.re)

im = Function(sym.im)

MatMul = Function(sym.MatMul)

MatAdd = Function(sym.MatAdd)

ui = unitimpulse = UnitImpulse = Function(UnitImpulse1)

us = unitstep = UnitStep = Function(UnitStep1)

rect = Function(rect1)

dtrect = Function(dtrect1)

dtsign = Function(dtsign1)

sinc = SincnFunction(sincn1)

sincn = SincnFunction(sincn1)

sincu = SincuFunction(sincu1)

psinc = PsincFunction(psinc1)

tri = Function(tri1)

trap = Function(trap1)

ramp = Function(ramp1)

rampstep = Function(rampstep1)

function_mapping = {sym.Heaviside: UnitStep1,
                    sym.DiracDelta: UnitImpulse1,
                    rect1: dtrect,
                    sym.sign: dtsign}

from .expr import Expr, expr, delcapify  # nopep8
