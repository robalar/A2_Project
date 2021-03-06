from ..core.numbers import Integer, Number, Undefined, Rational
from ..core.operations import Pow, base, exponent, Mul, Add, const, term
from ..core.expr import free_of_set
from ..core.simplify import auto_simplify

from math import factorial, floor


def is_mononomial_gpe(u, v):
    if not isinstance(v, set):
        variable_set = {v}
    else:
        variable_set = v

    if u in variable_set:
        return True

    elif isinstance(u, Pow):
        if base(u) in variable_set and isinstance(exponent(u), Integer) and exponent(u) > Number(1):  #FIXME
            return True
        else:
            return False

    elif isinstance(u, Mul):
        for operand in u.args:
            if not is_mononomial_gpe(operand, variable_set):
                return False
        return True

    return free_of_set(u, variable_set)


def is_polynomial_gpe(u, v):
    if not isinstance(v, set):
        variable_set = {v}
    else:
        variable_set = v

    if not isinstance(u, Add):
        return is_mononomial_gpe(u, set(variable_set))
    else:
        if u in variable_set:
            return True

        for operand in u.args:
            if not is_mononomial_gpe(operand, set(variable_set)):
                return False

        return True


def mononomials(u):
    if isinstance(u, Add):
        return set(u.args)
    else:
        return {u}


def variables(u):
    if isinstance(u, Add):
        v = set(u.args)
        return _variables_add(v)
    elif isinstance(u, Mul):
        v = set(u.args)
        return _variables_mul(v)
    else:
        return _variables({u})


def _variables_mul(u):
    sums = set([x for x in u if isinstance(x, Add)])
    v = u - sums
    return _variables(v) | sums


def _variables_add(u):
    v = set()
    for item in u:
        if isinstance(item, Mul):
            v |= _variables_mul(set(item.args))
        else:
            v |= _variables({item})

    return v


def _variables(u):
    v = set()
    for item in u:
        if isinstance(item, (Integer, Rational)):
            continue
        elif isinstance(item, Pow):
            if exponent(item) > Number(1):
                v |= {base(item)}
            else:
                v |= {item}
        else:
            v |= {item}
    return v


def coeff_var_monomial(u, s):
    """ Returns the coefficient and variable part of a monomial.

        Args:
            u: an algebraic expression
            s: (set of) generalised variable(s)
        Returns:
            Undefined if u is not a monomial in s
            Coefficient and variable part of u in form [[list of coefficients], [list of variables]]
    """
    if not isinstance(s, set):
        variable_set = {s}
    else:
        variable_set = s

    if not is_mononomial_gpe(u, variable_set):
        return Undefined()
    else:
        if isinstance(u, Mul):
            coeff_part = [c for c in u.args if free_of_set(c, variable_set)]
            var_part = [s for s in u.args if s not in coeff_part]

            if not var_part:
                var_part = [Number(1)]
            if not coeff_part:
                coeff_part = [Number(1)]

        else:
            coeff_part = [Number(1)]
            var_part = [u]

        return [auto_simplify(Mul(*coeff_part)), auto_simplify(Mul(*var_part))]


def collect_terms(u, variable_set):
    if not isinstance(u, Add):
        if isinstance(coeff_var_monomial(u, variable_set), Undefined):
            return Undefined()
        else:
            return u
    else:
        if u in variable_set:
            return u
        T = []
        for operand in u.args:
            f = coeff_var_monomial(operand, variable_set)
            if isinstance(f, Undefined):
                return Undefined()
            else:
                combined = False
                for i, other_operand in enumerate(T):
                    if f[1] == other_operand[1]:
                        T[i] = [f[0] + other_operand[0], f[1]]
                        combined = True
                        break
                if not combined:
                    T.append(f)

        v = Number(0)
        for item in T:
            v = v + item[0] * item[1]
        return v


def is_expanded(u):
    return not any(isinstance(x, Add) for x in variables(u))


def expand_product(r, s):
    if isinstance(r, Pow) and isinstance(s, Pow) and exponent(r) < Number(0) and exponent(s) < Number(0):
        return (expand_product(base(r)**abs(exponent(r)), base(s) ** abs(exponent(s))))**Number(-1)

    if isinstance(r, Add):
        if isinstance(s, Pow):
            return distribute(Mul(r, s))
        f = r.args[0]
        return expand_product(f, s) + expand_product(r - f, s)
    elif isinstance(s, Add):
        return expand_product(s, r)
    else:
        return r * s


def expand_power(u, n):

    if n < Number(0):
        return Number(1) / expand_power(_expand(u), abs(n))

    if isinstance(n, Rational):
        largest_int = Number(int(floor(n.value)))
        m = n - largest_int
        return expand_product(u ** m, expand_power(u, largest_int))

    if not isinstance(n, Integer):
        raise ValueError('n must be an integer, not {}'.format(repr(type(n))))
    elif n < Number(0):
        raise ValueError('n must be > 0, not {}'.format(n))

    if isinstance(u, Add):
        f = u.args[0]
        r = u - f
        s = Number(0)
        for k in range(n.value+1):
            c = Number(factorial(n.value)/(factorial(k) * factorial(n.value - k)))
            s = s + expand_product(c * f**Number(n.value-k), expand_power(r, Number(k)))
        return s
    else:
        return u**n


def _expand(u):
        if isinstance(u, Add):
            v = u.args[0]
            return _expand(v) + _expand(u - v)
        elif isinstance(u, Mul):
            v = u.args[0]
            return expand_product(_expand(v), _expand(u/v))
        elif isinstance(u, Pow):
            return expand_power(_expand(u.base), u.exponent)
        else:
            return u


def expand(u):
    # TODO: Make more efficient?
    v = _expand(u)
    while not is_expanded(v):
        v = _expand(v)
    return v


def distribute(u):
    if not isinstance(u, Mul):
        return u

    if not any(isinstance(x, Add) for x in u.args):
        return u

    v = next(x for x in u.args if isinstance(x, Add))
    f = Mul(*[x for x in u.args if x != v])
    s = Number(0)
    for item in v.args:
        s = s + item * f

    return s


# FIXME: Implement!
def degree_monomial(u):
    pass