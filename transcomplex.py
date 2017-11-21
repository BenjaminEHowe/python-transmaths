import transmaths
import cmath


class Transcomplex:
    """A transcomplex number. A transcomplex number is a polar vector of two transreal parts. """

    def __init__(self, *args):
        """Create a transcomplex number."""

        # first check what format the input number is in; in most cases this will be in polar form already; but for
        # the sake of completion we should accept a cmath 'complex number'.

        if isinstance(args[0], Transcomplex):
            # nothing to do here, really.
            self.magnitude = args[0].magnitude
            self.angle = args[0].angle
            return

        if isinstance(args[0], complex):
            try:
                self.polar = cmath.polar(args[0])
                print(self.polar)
            except TypeError:
                print("Error: Input was not a tuple or complex number of the form n+ij")
                return

            # We need, for transcomplex arithemtic, the polar form of the complex number.
            self.magnitude = self.polar[0]
            self.angle = self.polar[1]

            return

        # we have r and t as arguments. Lets make them transreal.
        # TODO: Add checks for correct types here.

        self.magnitude = args[0]
        self.angle = args[1]

        # if we've been provided two arguments, there's a possibility one is nullity.

        if self._check_nullity():
            # if this returns true, we're done building the transcomplex number
            return

        if self.angle == transmaths.INFINITY or self.angle == -transmaths.INFINITY:
            # any transcomplex number of angle infinity or -infinity is the point at nullity.

            self.magnitude = transmaths.NULLITY
            self.angle = 0

            return

        # any transcomplex number of magnitude zero is the point at zero (mag 0 ang 0)
        if self.magnitude == 0:
            self.angle = 0
            return

        try:
            self.magnitude = transmaths.Transreal(self.magnitude)
            self.angle = transmaths.Transreal(self.angle)
        except TypeError:
            print("Error: magnitude or angle are not numbers.")
            return

        print("real {}, imaginary {}".format(self.magnitude, self.angle))

        return

    def __mul__(self, other):
        # check that other is transcomplex

        try:
            other = Transcomplex(other)
        except TypeError:
            return NotImplemented

        magnitude = self.magnitude*other.magnitude

        angle = self.angle + other.angle

        ans = Transcomplex(magnitude, angle)

        # conform to convention for nullity angles.
        ans._check_nullity()

        return ans

    def __truediv__(self, other):

        # r1/r2 , theta1-theta2

        # check that both numbers are Transcomplex

        try:
            other = Transcomplex(other)
        except TypeError:
            return NotImplemented

        magnitude = self.magnitude/other.magnitude

        angle = self.angle - other.angle

        ans = Transcomplex(magnitude, angle)

        ans._check_nullity()

        return ans

    def __itruediv__(self, other):
        try:
            other = Transcomplex(other)
        except TypeError:
            return NotImplemented

        self.magnitude = self.magnitude/other.magnitude
        self.angle = self.angle/other.angle

        return self

    def __iadd__(self, other):
        try:
            other = Transcomplex(other)
        except TypeError:
            return NotImplemented



    def __add__(self, other):

        try:
            other = Transcomplex(other)
        except TypeError:
            return NotImplemented

        """Add two transcomplex numbers together. for adding real vectors, there is no reason not to use the cmath
        library for complex number addition. First here we should deal with the transreals; that is:
        - Nullity
        - Infinity + Infinity ( bisector )
        - Infinity + real finite number
        - Infinity + opposite Infinity ( Nullity )
        """

        # Nullity
        # if any part of either side of the calculation is nullity, the answer will be the point at nullity
        # hence (Nullity, 0)

        if self.magnitude == transmaths.NULLITY or self.angle == transmaths.NULLITY:
            return Transcomplex(transmaths.NULLITY, 0)

        if other.magnitude == transmaths.NULLITY or other.angle == transmaths.NULLITY:
            return Transcomplex(transmaths.NULLITY, 0)

        # as a third case, if the angle of either is infinity, it can be said to be nullity. thus the addition
        # will still yield (Nullity, 0)

        if self.angle == transmaths.INFINITY or other.angle == transmaths.INFINITY:
            return Transcomplex(transmaths.NULLITY, 0)

        # Adding opposite infinities

        if self.magnitude == transmaths.INFINITY and other.magnitude == transmaths.INFINITY:

            if self.magnitude.sign() > 0 > other.magnitude.sign():
                # Opposite infinities add to the point at nullity, hence Nullity,0
                return Transcomplex(transmaths.NULLITY, 0)
            if self.magnitude.sign() < 0 < other.magnitude.sign():
                return Transcomplex(transmaths.NULLITY, 0)

            # if we've reached this point, we have two, non-opposite infinities - we have to find their unique bisector



    def __repr__(self):
        """Transcomplex objects are not represented in a useful way on the command-line; overriding __repr__ allows
        us to see the magnitude and angle of the transcomplex number on the commandline rather than the name of the
        object."""

        return "({},{})".format(self.magnitude, self.angle)

    def polar(self):
        """return the polar form of the transcomplex number (r, t)"""

        return self.magnitude, self.angle

    def _check_nullity(self):
        """Just check that, if the magnitude of the transcomplex number is Nullity, the angle is 0 due to
        transmath convention."""

        if self.magnitude == transmaths.NULLITY or self.angle == transmaths.NULLITY:
            self.angle = 0
            self.magnitude = transmaths.NULLITY
            return True
        else:
            return False

    def _find_bisector(self, other):
        """Utility function for finding the unique bisector of two angles with magnitude infinity. """
