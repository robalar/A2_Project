from nose.tools import assert_equal, assert_is_instance

from solver.core.rationals import *
from solver.core.numbers import Undefined


def is_rationalized_test():

    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    d = Symbol('d')
    x = Symbol('x')
    y = Symbol('y')

    assert_equal(is_rationalized(a/b + c/d), False)
    assert_equal(is_rationalized((a*d + b*c)/(b*d)), True)

    assert_equal(is_rationalized(1 + 1/(1+1/a)), False)
    assert_equal(is_rationalized((2*a + 1)/(a + 1)), True)

    assert_equal(is_rationalized((((1/((x+y)**2+1))**Number(1,2)+1)*((1/((x+y)**2+1))**Number(1,2)-1))/(x+1)), True)


def rationalize_test():

    x = Symbol('x')
    a = Symbol('a')
    b = Symbol('b')
    c = Symbol('c')
    d = Symbol('d')

    assert_equal(rationalise((1+1/x)**2), ((x+1)**2)/x**2)
    assert_equal(rationalise((1+1/x)**Number(1,2)), ((x+1)/x)**Number(1,2))
    assert_equal(rationalise(a/b + c/d), (a*d + b*c)/(b*d))
    assert_equal(rationalise(1/(1 + 1/x)**Number(1,2)+ (1+1/x)**Number(3,2)), (x**2 + (x+1)**2)/(x**2*((x+1)/x)**Number(1,2)))


def rational_expand_test():

    x = Symbol('x')
    y = Symbol('y')

    v = ((1/((x+y)**2+1))**Number(1, 2)+1)*((1/((x+y)**2+1))**Number(1, 2)-1)/(x+1)
    assert_equal(rational_expand(v), (-x**2 - 2*x*y - y**2)/(x**3 + x**2 + 2*x**2*y + 2*x*y + x*y**2 +y**2 + x + 1))

    assert_is_instance(rational_expand(1/(x**2+x-x*(x+1))), Undefined)