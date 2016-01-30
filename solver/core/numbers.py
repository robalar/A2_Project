from .atoms import Atom


class Number(Atom):

    def __new__(cls, *args):

        if len(args) == 1:

            if isinstance(args[0], Number):
                return args[0]
            if isinstance(args[0], int):
                return super(Number, cls).__new__(Integer)

    def __repr__(self):
        return str(self.value)


class Undefined(Number):
    """ For calculations where the result is known i.e. 0/0, 0^0, oo/oo
    """

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __div__(self, other):
        return self


class Integer(Number):

    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value)
        else:
            Atom.__add__(self, other)

    def __iadd__(self, other):
        return self + other

    def __mul__(self, other):
        if isinstance(other, Integer):
            return Integer(self.value * other.value)
        else:
            Atom.__mul__(self, other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, power, modulo=None):

        if isinstance(power, Integer):
            if power.value == 0 and self.value == 0:
                return Undefined()

            return Integer(self.value ** power.value)
        else:
            Atom.__pow__(self, power)

    def __eq__(self, other):

        if isinstance(other, Integer):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)