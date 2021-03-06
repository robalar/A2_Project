from nose.tools import assert_equal

from solver.polynomials.general_polynomial import *
from solver.core.symbol import Symbol
from solver.trigonometry.functions import sin

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')
a = Symbol('a')
b = Symbol('b')
c = Symbol('c')
n = Symbol('n')


def is_mononomial_gpe_test():
    assert_equal(is_mononomial_gpe(x**Number(2), x), True)
    assert_equal(is_mononomial_gpe(a*x**Number(2)*y**Number(2), {x,y}), True)
    assert_equal(is_mononomial_gpe(x**Number(2)+y**Number(2), {x, y}), False)


def is_polynomial_gpe_test():
    assert_equal(is_polynomial_gpe(a+b, {a+b}), True)
    assert_equal(is_polynomial_gpe(x**Number(2)+y**Number(2), {x, y}), True)
    assert_equal(is_polynomial_gpe(sin(x)**Number(2) + Number(2)*sin(x) + Number(3), sin(x)), True)
    assert_equal(is_polynomial_gpe(x/y + Number(2)*y, {x,y}), False)
    assert_equal(is_polynomial_gpe((x+Number(1))*(x+Number(3)), x), False)


def variables_test():
    assert_equal(variables(Number(3)*x*(x+Number(1))*y**Number(2)*z**n), {x, x + Number(1), y, z**n})
    assert_equal(variables(a*sin(x)**Number(2)+Number(2)*b*sin(x)+Number(3)*c), {a, b, c, sin(x)})
    assert_equal(variables(Number(2)**Number(1, 2)*x**Number(2) + Number(3)**Number(1, 2) + Number(5)**Number(1, 2)),
                 {x, Number(2)**Number(1, 2), Number(3)**Number(1, 2), Number(5)**Number(1, 2)})
    assert_equal(variables(Number(1,2)), set())
    assert_equal(variables(x*Number(3)+Number(3)*x**Number(2)*y + Number(3)*x*y**Number(2)+y**Number(3)), {x, y})
    assert_equal(variables(4*x*(x+5)), {x, x+5})


def coeff_var_monomial_test():
    assert_equal(isinstance(coeff_var_monomial(Number(3)*x**Number(3)+Number(2)*x, x), Undefined), True)
    assert_equal(coeff_var_monomial(Number(3)*x*y**Number(2), {x,y}), [Number(3), x*y**Number(2)])
    assert_equal(coeff_var_monomial(x**Number(3), x), [Number(1), x**Number(3)])


def collect_terms_test():
    assert_equal(collect_terms((Number(2)*a + Number(3)*b)*x*y + (Number(4)*a+Number(5)*b)*x, {x, y}), (Number(2)*a + Number(3)*b)*x*y + (Number(4)*a+Number(5)*b)*x)
    assert_equal(collect_terms(Number(2)*a*x*y + Number(3)*b*x*y + Number(4)*a*x + Number(5)*b*x, {x, y}), (Number(2)*a + Number(3)*b)*x*y + (Number(4)*a+Number(5)*b)*x)
    assert_equal(isinstance(collect_terms(Number(3)*x**Number(2), y), Undefined), True)
    assert_equal(collect_terms(Number(3)*x**Number(2), x), Number(3)*x**Number(2))
    assert_equal(isinstance(collect_terms(y**Number(2)+y*Number(3), {x}), Undefined), True)


def is_expanded_test():
    assert_equal(is_expanded(x**3 + 4*x + 5), True)
    assert_equal(is_expanded(x**2 + x*(x + 6)*y), False)


def expand_test():
    assert_equal(expand((x+3)*(x+2)**2), x**3 + 7*x**2 + 16*x + 12)
    assert_equal(expand(1/((x+3)*(x+4))), 1/(x**2 + 7*x + 12))
    assert_equal(expand(a*(b+c)), a*b + a*c)
    assert_equal(expand(1/(a*(b+c))), 1/(a*b + a*c))
    assert_equal(expand((x+2)**Number(5,2)), (x+2)**Number(1,2)*x**2 + (x+2)**Number(1,2)*4*x + 4*(x+2)**Number(1,2))
    assert_equal(expand((x*(y+1)**Number(3,2)+1)*(x*(y+1)**Number(3,2)-1)), x**2*y**3 + 3*x**2*y**2+3*x**2*y+x**2-1)
    assert_equal(expand((x*(y+1)**Number(1,2)+1)**4), x**4*y**2+2*x**4*y+x**4+4*x**3*y*(y+1)**Number(1,2)+4*x**3*(y+1)**Number(1,2)+6*x**2*y+6*x**2+4*x*(y+1)**Number(1,2)+1)

def mononomials_test():
    assert_equal(mononomials(x), {x})
    assert_equal(mononomials(x**2 + 3*y + 6), {x**2, 3*y, Number(6)})
