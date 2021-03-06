from .base import Atom
from fractions import Fraction, gcd
from .common import convert_method_args
from .symbol import Undefined, Symbol

@convert_method_args()
class Number(Atom):

    def __new__(cls, *args):

        if cls is Number:
            if len(args) == 1:
                arg = args[0]

                if isinstance(arg, (int, long)):
                    return super(Number, cls).__new__(Integer, arg)
                elif isinstance(arg, (basestring, float)):
                    return super(Number, cls).__new__(Rational, arg)
                elif isinstance(arg, Fraction):
                    if arg.denominator == 1:
                        return super(Number, cls).__new__(Integer, arg.numerator)
                    else:
                        return super(Number, cls).__new__(Rational, arg)

            if len(args) == 2:
                return super(Number, cls).__new__(Rational, *args)

        else:
            return super(Number, cls).__new__(cls, *args)

    def __mul__(self, other):

        if isinstance(other, Number):
            return Number(self.value * other.value)

        return super(Number, self).__mul__(other)

    def __pow__(self, power, modulo=None):

        from .operations import denominator

        if isinstance(power, Integer):
            if power < Number(0) and self == Number(0):
                return Undefined()
            else:
                return Number(self.value ** power.value)
        elif isinstance(power, Rational) and is_nth_root(self, denominator(power)):
            v = self.value ** power.value
            return Number(v)

        return super(Number, self).__pow__(power)

    def __add__(self, other):

        if isinstance(other, Number):
            return Number(self.value + other.value)

        return super(Number, self).__add__(other)

    def __iadd__(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)

        return super(Number, self).__add__(other)

    def __eq__(self, other):
        if isinstance(other, Number):
            return self.value == other.value
        else:
            return super(Number, self).__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, Number):
            return self.value < other.value
        else:
            return False

    def __hash__(self):
        return hash(self.value)

    def __abs__(self):
        return Number(abs(self.value))

    @property
    def basic_string(self):
        return str(self.value)

    @property
    def latex(self):
        return self.basic_string

    def __repr__(self):
        return repr(self.value)

class Integer(Number):

    def __init__(self, value):
        super(Integer, self).__init__()
        self.value = value


class Rational(Number):
    """ Purely a wrapper for the builtin fraction class
    """

    def __init__(self, *args):

        self.value = Fraction(*args).limit_denominator()
        super(Rational, self).__init__()

        self.numerator = self.value.numerator
        self.denominator = self.value.denominator

    def __str__(self):
        return self.value.__str__()


def is_nth_root(value, root):

    if not isinstance(value, Number) or not isinstance(root, Number):
        raise ValueError('value and root must both be Numbers not {} and {}'.format(type(value), type(root)))

    u = value.value ** (1.0/root.value)
    u = long(round(u))
    return u ** root.value == value.value


# TODO: Redo
@convert_method_args()
class ReservedSymbol(Symbol, Number):
    """ Used to represent numbers like pi and e that have values but are imprecise.

        Attributes:
            name: name of the symbol
            value: approximate value of the symbol
    """
    def __init__(self, name, value):
        super(ReservedSymbol, self).__init__(name)
        self.value = value

    def __eq__(self, other):
        if isinstance(other, ReservedSymbol):
            return self.name == other.name
        elif isinstance(other, Number):
            return other.value == self.value
        else:
            return super(ReservedSymbol, self).__eq__(other)

    def __lt__(self, other):
        if isinstance(other, ReservedSymbol):
            return self.name < other.name
        elif isinstance(other, Number):
            return self.value < other.value
        else:
            return super(ReservedSymbol, self).__lt__(other)


def lcm(*values):

    if len(values) == 2:

        m = values[0]
        n = values[1]

        if not(isinstance(m, Integer) and isinstance(n, Integer)):
            raise ValueError('lcm is only defined for integer values')

        return abs(m * n)/gcd(m.value, n.value)
    else:
        return lcm(values[0], lcm(*values[1:]))