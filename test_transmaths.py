"""Unit tests for the transmaths module."""
import unittest
import transmaths

Transreal = transmaths.Transreal

class TestTransreal(unittest.TestCase):
    """Tests the Transreal object."""

    def test_add_exception(self):
        """Strings cannot be added to transreal numbers."""
        with self.assertRaises(TypeError):
            Transreal(1) + "one"

    def test_add_nullity(self):
        """nullity + x = nullity."""
        self.assertEqual(transmaths.NULLITY + 1, transmaths.NULLITY)

    def test_eq_exception(self):
        """Transreal numbers are not equal to strings."""
        self.assertNotEqual(Transreal(2), "two")

    def test_eq_negation(self):
        """Different transreal numbers are not equal."""
        self.assertNotEqual(Transreal(1), Transreal(2))

    def test_float(self):
        """Transreal numbers can be converted to floats."""
        self.assertTrue(isinstance(float(Transreal(1, 3)), float))

    def test_floordiv_exception(self):
        """Floor division of a transreal and a string is not possible."""
        with self.assertRaises(TypeError):
            Transreal(1) // "foo"

    def test_ge(self):
        """Transreal numbers can be compared using "greater than or equal to"."""
        self.assertGreaterEqual(Transreal(3), 1)

    def test_gt_exception(self):
        """Transreal numbers cannot be compared to strings."""
        with self.assertRaises(TypeError):
            Transreal(1) > "foo"

    def test_gt_nullity(self):
        """Nullity is not greater than any transreal number."""
        self.assertFalse(Transreal(1) > transmaths.NULLITY)

    def test_iadd(self):
        """In-place addition."""
        t = Transreal(1)
        t += 1
        self.assertEqual(t, 2)

    def test_ifloordiv(self):
        """In-place floor division."""
        t = Transreal(5)
        t //= 2
        self.assertEqual(t, 2)

    def test_init_exceptions(self):
        """Initialising a transreal incorrectly raises an exception."""
        # non-int denominator
        with self.assertRaises(TypeError):
            Transreal(1, float(1/2))

    def test_init_float_inf(self):
        """Initialise a transreal number from float infinity."""
        t = Transreal(float("inf"))
        self.assertEqual(t.numerator, 1)
        self.assertEqual(t.denominator, 0)

    def test_init_float_ninf(self):
        """Initialise a transreal number from float negative infinity."""
        t = Transreal(float("-inf"))
        self.assertEqual(t.numerator, -1)
        self.assertEqual(t.denominator, 0)

    def test_init_improper(self):
        """Initialise a transreal number from an improper fraction."""
        t = Transreal(1, -2)
        self.assertEqual(t.numerator, -1)
        self.assertEqual(t.denominator, 2)

    def test_init_infinity_precision(self):
        """Initalise transreal infinity from a transreal number and an imprecice number."""
        self.assertFalse(Transreal(Transreal(2).root(2), 0).approximate)

    def test_init_transreal_int(self):
        """Initialise a transreal number from a transreal numerator and a int denominator."""
        t = Transreal(Transreal(4), 2)
        self.assertEqual(t.numerator, 2)
        self.assertEqual(t.denominator, 1)

    def test_int(self):
        """Transreal numbers can be converted to integers."""
        self.assertEqual(int(Transreal(3, 2)), 1)

    def test_imod(self):
        """In-place modulo arithmetic."""
        t = Transreal(5)
        t %= 3
        self.assertEqual(t, 2)

    def test_ipow(self):
        """In-place powers."""
        t = Transreal(2)
        t **= 2
        self.assertEqual(t, 4)

    def test_isub(self):
        """In-place subtraction."""
        t = Transreal(2)
        t -= 1
        self.assertEqual(t, 1)

    def test_itruediv(self):
        """In-place (true) division."""
        t = Transreal(1)
        t /= 2
        self.assertEqual(t, 0.5)

    def test_le(self):
        """Transreal numbers can be compared using "less than or equal to"."""
        self.assertLessEqual(Transreal(1), Transreal(2))

    def test_lt_exception(self):
        """Transreal numbers cannot be compared to strings."""
        with self.assertRaises(TypeError):
            Transreal(1) < "foo"

    def test_mod_exception(self):
        """Modulo arithmetic doesn't work with transreal numbers and strings."""
        with self.assertRaises(TypeError):
            Transreal(5) % "three"

    def test_mul_exception(self):
        """Transreal numbers cannot be multiplied by strings."""
        with self.assertRaises(TypeError):
            Transreal(2) * "two"

    def test_pos(self):
        """Test the positive unary operator "yields its numeric argument unchanged"."""
        self.assertEqual(+Transreal(1), 1)

    def test_pow_exception(self):
        """Transreal numbers cannot be raised to strings."""
        with self.assertRaises(TypeError):
            Transreal(1) ** "foo"

    def test_pow_mod(self):
        """Three argument pow (self, power, modulus) is supported."""
        self.assertEqual(pow(Transreal(64), 6, 9), 1)

    def test_pow_nullity_1(self):
        """nullity**0 == nullityIf the power is zero, the result is (mostly) 1."""
        self.assertEqual(transmaths.NULLITY ** 0, transmaths.NULLITY)

    def test_pow_real_1(self):
        """If the power is zero, the result is (mostly) 1."""
        self.assertEqual(Transreal(64) ** 0, 1)

    def test_pow_real_gt1(self):
        """If the power is not whole and greater than 1, the result is the product of whole and fractional powers."""
        t = Transreal(2)**Transreal(5, 3)
        self.assertGreater(t, 3.17)
        self.assertLess(t, 3.18)

    def test_pow_real_nullity(self):
        """If the power is nullity, the result is nullity."""
        self.assertEqual(Transreal(2) ** transmaths.NULLITY, transmaths.NULLITY)

    def test_pow_real1_infinity(self):
        """If the power is infinity and the number is 1, the result is nullity."""
        self.assertEqual(Transreal(1) ** transmaths.INFINITY, transmaths.NULLITY)

    def test_pow_realgt1_infinity(self):
        """If the power is infinity and the number is greater than 1, the result is infinity."""
        self.assertEqual(Transreal(2) ** transmaths.INFINITY, transmaths.INFINITY)

    def test_pow_reallt1_infinity(self):
        """If the power is infinity and the number is less than 1, the result is zero."""
        self.assertEqual(Transreal(1, 2) ** transmaths.INFINITY, 0)

    def test_rdivmod(self):
        """Divmod can be calculated with reversed operands."""
        self.assertEqual(divmod(5, Transreal(2)), (2, 1))

    def test_rdivmod_exception(self):
        """Reversed operands don't allow divmod of strings."""
        with self.assertRaises(TypeError):
            divmod("foo", Transreal(2))

    def test_rmod(self):
        """The modulus can be calculated with reverse operands."""
        self.assertEqual(5 % Transreal(3), 2)

    def test_rmod_exception(self):
        """Reversed operands don't allow the modulus of sets to be calculated."""
        with self.assertRaises(TypeError):
            set() % Transreal(3)

    def test_rpow(self):
        """Powers can be calculated with reversed operands."""
        self.assertEqual(2 ** Transreal(2), 4)

    def test_rpow_exception(self):
        """Reversed operands don't allow strings to be raised to powers."""
        with self.assertRaises(TypeError):
            "foo" ** Transreal(2)

    def test_rsub(self):
        """Subtraction with reversed operands works."""
        self.assertEqual(2 - Transreal(1), 1)

    def test_rsub_exception(self):
        """Reversed operands don't allow transreal numbers to be subtracted from strings."""
        with self.assertRaises(TypeError):
            "foo" - Transreal(2)

    def test_rtruediv(self):
        """(true) Division with reversed operands works."""
        self.assertEqual(1 / Transreal(3), Transreal(1, 3))

    def test_rtruediv_exception(self):
        """Reversed operands don't allow strings to be divided by transreal numbers."""
        with self.assertRaises(TypeError):
            "foo" / Transreal(2)

    def test_root_exact(self):
        """The cube root of 64 is exactly 4 (not 3.9999999999999996)."""
        self.assertEqual(Transreal(64).root(3), 4)

    def test_root_infinity(self):
        """The square root of infinity is infinity."""
        self.assertEqual(transmaths.INFINITY.root(2), transmaths.INFINITY)

    def test_root_infinity_infinity(self):
        """The infinite root of infinity is nullity."""
        self.assertEqual(transmaths.INFINITY.root(transmaths.INFINITY), transmaths.NULLITY)

    def test_root_infinity_real(self):
        """The infinite root of a real number is 0."""
        self.assertEqual(Transreal(1).root(transmaths.INFINITY), 0)

    def test_root_negative(self):
        """The square root of -1 should be a complex number, but for now is nullity."""
        self.assertEqual(Transreal(-1).root(2), transmaths.NULLITY)

    def test_root_negative_infinity(self):
        """The negative second root of infinity is -infinity."""
        self.assertEqual(transmaths.INFINITY.root(-2), -transmaths.INFINITY)

    def test_root_nullity(self):
        """The square root of nullity is nullity."""
        self.assertEqual(transmaths.NULLITY.root(2), transmaths.NULLITY)

    def test_sign_negative(self):
        """Test the sign function for negative numbers."""
        self.assertEqual(Transreal(-1).sign(), -1)

    def test_sign_nullity(self):
        """Test the sign function for nullity."""
        self.assertEqual(transmaths.NULLITY.sign(), transmaths.NULLITY)

    def test_sign_positive(self):
        """Test the sign function for positive numbers."""
        self.assertEqual(Transreal(1).sign(), 1)

    def test_sign_zero(self):
        """Test the sign function for zero."""
        self.assertEqual(Transreal(0).sign(), 0)

    def test_str_approx(self):
        """Approximate transreal numbers are prefixed by a tilde."""
        self.assertEqual(str(Transreal(2).root(2)), "~707106781/500000000")

    def test_str_inf(self):
        """Convert infinity to a string."""
        self.assertEqual(str(Transreal(1, 0)), "infinity")

    def test_str_int(self):
        """Convert a transreal integer to a string."""
        self.assertEqual(str(Transreal(2)), "2")

    def test_str_ninf(self):
        """Convert minus infinity to a string."""
        self.assertEqual(str(Transreal(-1, 0)), "-infinity")

    def test_str_nullity(self):
        """Convert nullity to a string."""
        self.assertEqual(str(Transreal(0, 0)), "nullity")

    def test_sub_exception(self):
        """Strings cannot be subtracted from other numbers."""
        with self.assertRaises(TypeError):
            Transreal(1) - "one"

    def test_truediv_exception(self):
        """Transreal numbers cannot be divided by strings."""
        with self.assertRaises(TypeError):
            Transreal(2) / "two"


if __name__ == "__main__":
    unittest.main()
