"""Allows the use of transmathematics (https://bh96.link/transmaths) in Python."""
from math import gcd

# see https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types
class Transreal:
    """A transreal number."""

    def __init__(self, numerator, denominator=1, approximate=False):
        """Initialise a transreal number based on a numerator and denominator."""
        # if the numerator or the denominator are transreal, just do the maths
        if isinstance(numerator, Transreal) or isinstance(denominator, Transreal):
            if denominator == 1:
                self.numerator = numerator.numerator
                self.denominator = numerator.denominator
                self.approximate = numerator.approximate
            else:
                result = numerator / denominator
                self.numerator = result.numerator
                self.denominator = result.denominator
                self.approximate = result.approximate
            return

        # check numerator and denominator are integers
        if not isinstance(denominator, int):
            raise TypeError("The denominator must be an int!")
        if not isinstance(numerator, int):
            if isinstance(numerator, float):
                try:
                    self.numerator, self.denominator = (numerator).as_integer_ratio()
                    self.approximate = True
                except OverflowError:
                    # this means that the numerator is + or - infinity
                    if numerator == float("inf"):
                        self.numerator = 1
                        self.denominator = 0
                        self.approximate = False
                    elif numerator == float("-inf"):
                        self.numerator = -1
                        self.denominator = 0
                        self.approximate = False
                    else: # pragma: no cover (we should never hit this...)
                        raise
                return
            else:
                raise TypeError("The numerator must be an int or float!")

        # check the fraction won't be improper, multiply numerator and denominator by -1 if required
        if denominator < 0:
            numerator *= -1
            denominator *= -1

        # simplify the numerator and denominator if possible
        common_factor = gcd(numerator, denominator)
        if common_factor > 1:
            numerator = numerator // common_factor
            denominator = denominator // common_factor

        # set the values
        self.numerator = numerator
        self.denominator = denominator
        self.approximate = approximate
        return


    def __abs__(self):
        if self.numerator < 0:
            return -self
        else:
            return self


    def __add__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        # if the denominators are the same, add the fractions simply
        if self.denominator == other.denominator:
            return Transreal(
                self.numerator + other.numerator,
                self.denominator,
                self.approximate or other.approximate)
        else:
            return Transreal(
                (self.numerator * other.denominator) + (other.numerator * self.denominator),
                self.denominator * other.denominator,
                self.approximate or other.approximate
            )


    def __divmod__(self, other):
        floordiv = self // other
        mod = self - (other * floordiv)
        return (floordiv, mod)


    def __eq__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return self.numerator == other.numerator and self.denominator == other.denominator


    def __float__(self):
        return self.numerator / self.denominator


    def __floordiv__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return (self / other).floor()


    def __ge__(self, other):
        return self > other or self == other


    def __gt__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        if self == NULLITY or other == NULLITY:
            return False
        elif self.denominator == other.denominator:
            return self.numerator > other.numerator
        else:
            return self.numerator * other.denominator > other.numerator * self.denominator


    def __iadd__(self, other):
        self = self + other
        return self


    def __ifloordiv__(self, other):
        self = self // other
        return self


    def __imod__(self, other):
        self = self % other
        return self


    def __imul__(self, other):
        self = self * other
        return self


    def __int__(self):
        return self.numerator // self.denominator


    def __ipow__(self, other):
        self = self ** other
        return self


    def __isub__(self, other):
        self = self - other
        return self


    def __itruediv__(self, other):
        self = self / other
        return self


    def __le__(self, other):
        return self < other or self == other


    def __lt__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        if self == NULLITY or other == NULLITY:
            return False
        elif self.denominator == other.denominator:
            return self.numerator < other.numerator
        else:
            return self.numerator * other.denominator < other.numerator * self.denominator


    def __mod__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return self - (other * (self // other))


    def __mul__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return Transreal(
            self.numerator * other.numerator,
            self.denominator * other.denominator,
            self.approximate or other.approximate)


    def __ne__(self, other):
        return not self == other


    def __neg__(self):
        return self * -1


    def __pos__(self):
        # "yields its numeric argument unchanged" (yes, this seems insane...)
        # https://docs.python.org/3/reference/expressions.html#unary-arithmetic-and-bitwise-operations
        return self


    def __pow__(self, power, modulo=None):
        # if the power isn't transreal, try to make it transreal
        try:
            power = Transreal(power)
        except TypeError:
            return NotImplemented

        # if the power is negative, invert the fraction and make the power positive
        if power < 0:
            self = Transreal(self.denominator, self.numerator, self.approximate)
            power *= -1

        # if the power is zero, the result is (mostly) 1
        if power == 0:
            if self == 0 or self == NULLITY:
                raised = NULLITY
            else:
                raised = 1

        # if the power is less than 1 (can't be a whole number, must be between 0 and 1)
        elif power < 1:
            raised = (self ** power.numerator).root(power.denominator)

        # if the power is 1, the result is (mostly) self
        elif power == 1:
            raised = self

        # if the power is nullity, the result is nullity
        elif power == NULLITY:
            raised = NULLITY

        # if the power is infinity, the result is...
        elif power == INFINITY:
            # nullity if the absolute value of self is less than 1
            if abs(self) < 1:
                raised = 0
            # 1 if the absolute value of self is equal to 1
            elif abs(self) == 1:
                raised = NULLITY
            # infinity if the absolute value is self is greater than 1
            else:
                raised = INFINITY

        # if the power is a whole number
        elif power.denominator == 1:
            raised = Transreal(
                self.numerator ** power.numerator,
                self.denominator ** power.numerator,
                self.approximate or power.approximate)

        # the power is not a whole number and greater than 1
        else:
            whole, fraction = divmod(power.numerator, power.denominator)
            fraction = Transreal(fraction, power.denominator, power.approximate)
            raised = (self ** whole) * (self ** fraction)

        if modulo is None:
            return raised
        else:
            return raised % modulo


    def __str__(self):
        string = ""
        # if the number is approximate, prefix with a tilde
        if self.approximate:
            string += "~"

        # if the denominator is 1, it's an integer so just print the numerator
        if self.denominator == 1:
            string += str(self.numerator)

        # if the denominator is 0, work out if it's -infinity, infinity, or nullity
        elif self.denominator == 0:
            if self.numerator < 0:
                string += "-infinity"
            elif self.numerator > 0:
                string += "infinity"
            else:
                string += "nullity"

        # for all other denominators, print the fraction
        else:
            string += str(self.numerator) + "/" + str(self.denominator)

        # return the string we built
        return string


    def __sub__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return self + (other * -1)


    def __truediv__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        # multiply self by the inverse of other
        return self * (other ** -1)


    def __rdivmod__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return divmod(other, self)


    __repr__ = __str__


    __radd__ = __add__


    def __rmod__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return other % self


    __rmul__ = __mul__


    def __rpow__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return other ** self


    def __rsub__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return other - self


    def __rtruediv__(self, other):
        # if other isn't transreal, try to make it transreal
        try:
            other = Transreal(other)
        except TypeError:
            return NotImplemented

        return other / self


    def floor(self):
        """Return the floor of (the largest integer value less than or equal to) self."""
        # for non-finite numbers or numbers with a denominator of 1 just return the number
        if self.denominator == 0 or self.denominator == 1:
            return self
        else:
            return Transreal(self.numerator // self.denominator, approximate=self.approximate)


    def root(self, power):
        """Returns the power-th root of self using Newton's method."""
        PRECISION = 9 # accurate to 1 billionth

        # source: http://mathforum.org/library/drmath/view/52628.html
        prev_guess = Transreal(0)
        guess = Transreal(1)

        while Transreal(1, 10**PRECISION) < abs(guess - prev_guess):
            prev_guess = guess.round(PRECISION * 2)
            guess = prev_guess - (prev_guess**power - self)/(power * prev_guess**(power-1))

        result = guess.round(PRECISION)

        if result ** power == self:
            return result
        else:
            result.approximate = True
            return result


    def round(self, decimal_places):
        """Returns self rounded to the specified number of decimal places."""
        rounded = (self * 10**(decimal_places)).floor() / 10**(decimal_places)
        return rounded



INFINITY = Transreal(1, 0)
NULLITY = Transreal(0, 0)
PI = Transreal(3141592653589793238462643, 10**24, approximate=True)
