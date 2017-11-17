"""Unit tests confirming the axioms of transreal arithmetic hold true for the transmaths module."""
import unittest
import transmaths

Transreal = transmaths.Transreal

transreals = [
    transmaths.NULLITY,
    -transmaths.INFINITY,
    -Transreal(3, 2),
    -(Transreal(2).root(2)),
    -Transreal(1),
    -Transreal(1, 3),
    Transreal(0),
    Transreal(1, 3),
    Transreal(1),
    Transreal(2).root(2),
    Transreal(3, 2),
    transmaths.INFINITY
]

class TestTransrealAxioms(unittest.TestCase):
    """Tests the Transreal object obeys the axioms of transreal arithmetic."""

    def test_a01(self):
        """Test additive associativity."""
        for a in transreals:
            for b in transreals:
                for c in transreals:
                    self.assertEqual(a + (b + c), (a + b) + c)

    def test_a02(self):
        """Test additive commutativity."""
        for a in transreals:
            for b in transreals:
                self.assertEqual(a + b, b + a)

    def test_a03(self):
        """Test additive identity."""
        for a in transreals:
            self.assertEqual(0 + a, a)

    def test_a04(self):
        """Test additive nullity."""
        for a in transreals:
            self.assertEqual(transmaths.NULLITY + a, transmaths.NULLITY)

    def test_a05(self):
        """Test additive infinity."""
        for a in transreals:
            if a == -transmaths.INFINITY or a == transmaths.NULLITY:
                continue
            self.assertEqual(a + transmaths.INFINITY, transmaths.INFINITY)

    def test_a06(self):
        """Test subtraction as sum with opposite."""
        for a in transreals:
            for b in transreals:
                self.assertEqual(a - b, a + (-b))

    def test_a07(self):
        """Test bijectivity of opposite."""
        for a in transreals:
            self.assertEqual(-(-a), a)

    def test_a08(self):
        """Test additive inverse."""
        for a in transreals:
            if abs(a) == transmaths.INFINITY or a == transmaths.NULLITY:
                continue
            self.assertEqual(a - a, 0)

    def test_a09(self):
        """Test opposite of nullity."""
        self.assertEqual(-transmaths.NULLITY, transmaths.NULLITY)

    def test_a10(self):
        """Test non-null subtraction of infinity."""
        for a in transreals:
            if abs(a) == transmaths.INFINITY or a == transmaths.NULLITY:
                continue
            self.assertEqual(a - transmaths.INFINITY, -transmaths.INFINITY)

    def test_a11(self):
        """Test subtraction of infinity from infinity."""
        self.assertEqual(transmaths.INFINITY - transmaths.INFINITY, transmaths.NULLITY)

    def test_a12(self):
        """Test multiplicative associativity."""
        for a in transreals:
            for b in transreals:
                for c in transreals:
                    self.assertEqual(a * (b * c), (a * b) * c)

    def test_a13(self):
        """Test multiplicative commutativity."""
        for a in transreals:
            for b in transreals:
                self.assertEqual(a * b, b * a)

    def test_a14(self):
        """Test multiplicative identity."""
        for a in transreals:
            self.assertEqual(1 * a, a)

    def test_a15(self):
        """Test multiplicative nullity."""
        for a in transreals:
            self.assertEqual(transmaths.NULLITY * a, transmaths.NULLITY)

    def test_a16(self):
        """Test infinity times zero."""
        self.assertEqual(transmaths.INFINITY * 0, transmaths.NULLITY)

    def test_a17(self):
        """Test division."""
        for a in transreals:
            for b in transreals:
                self.assertEqual(a / b, a * b**-1)

    def test_a18(self):
        """Test multiplicative inverse."""
        for a in transreals:
            if a == 0 or abs(a) == transmaths.INFINITY or a == transmaths.NULLITY:
                continue
            self.assertEqual(a / a, 1)

    def test_a19(self):
        """Test bijectivity of reciprocal."""
        for a in transreals:
            if a == -transmaths.INFINITY:
                continue
            self.assertEqual((a ** -1) ** -1, a)

    def test_a20(self):
        """Test reciprocal of zero."""
        self.assertEqual(Transreal(0) ** -1, transmaths.INFINITY)

    def test_a21(self):
        """Test reciprocal of the opposite of infinity."""
        self.assertEqual((-transmaths.INFINITY) ** -1, 0)

    def test_a22(self):
        """Test reciprocal of nullity."""
        self.assertEqual(transmaths.NULLITY ** -1, transmaths.NULLITY)

    def test_a23(self):
        """Test positive."""
        for a in transreals:
            if a > 0:
                self.assertEqual(transmaths.INFINITY * a, transmaths.INFINITY)
            if transmaths.INFINITY * a == transmaths.INFINITY:
                self.assertGreater(a, 0)

    def test_a24(self):
        """Test negative."""
        for a in transreals:
            if 0 > a:
                self.assertEqual(transmaths.INFINITY * a, -transmaths.INFINITY)
            if transmaths.INFINITY * a == -transmaths.INFINITY:
                self.assertGreater(0, a)

    def test_a25(self):
        """Test positive infinity."""
        self.assertGreater(transmaths.INFINITY, 0)

    def test_a26(self):
        """Test ordering."""
        for a in transreals:
            for b in transreals:
                if a - b > 0:
                    self.assertGreater(a, b)
                if a > b:
                    self.assertGreater(a - b, 0)

    def test_a27(self):
        """Test less than."""
        for a in transreals:
            for b in transreals:
                if a > b:
                    self.assertLess(b, a)
                if b < a:
                    self.assertGreater(a, b)

    def test_a28(self):
        """Test greater than or equal."""
        for a in transreals:
            for b in transreals:
                if a >= b:
                    self.assertTrue(a > b or a == b)
                if a > b or a == b:
                    self.assertGreaterEqual(a, b)

    def test_a29(self):
        """Test less than or equal."""
        for a in transreals:
            for b in transreals:
                if a <= b:
                    self.assertGreaterEqual(b, a)
                if b >= a:
                    self.assertLessEqual(a, b)

    def test_a30(self):
        """Test quadrachotomy."""
        for a in transreals:
            self.assertTrue(a < 0 or a == 0 or a > 0 or a == transmaths.NULLITY)

    def test_a31(self):
        """Test distributivity."""
        for a in transreals:
            for b in transreals:
                for c in transreals:
                    if not ((abs(a) == transmaths.INFINITY and (b.sign() != c.sign())) and (b + c != 0 or b + c != transmaths.NULLITY)):
                        self.assertEqual(a * (b + c), (a * b) + (a * c))


if __name__ == "__main__":
    unittest.main()
