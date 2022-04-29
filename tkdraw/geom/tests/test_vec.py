import unittest
import math

from .. import Vec


class TestVec(unittest.TestCase):
    def test_eq(self):
        v0 = Vec(1, 2)
        v1 = Vec(1., 2.)
        v2 = Vec(2, 1)
        self.assertEqual(v0, v1)
        self.assertFalse(v0 == v2)

    def test_ne(self):
        v0 = Vec(1, 2)
        v1 = Vec(1., 2.)
        v2 = Vec(2, 1)
        self.assertNotEqual(v0, v2)
        self.assertFalse(v0 != v1)

    def test_add(self):
        v0 = Vec(12, 34)
        v1 = Vec(56, 78)
        v2 = Vec(-910, -1112)
        v3 = Vec(12 + 56, 34 + 78)
        v4 = Vec(12 - 910, 34 - 1112)
        self.assertEqual(v0 + v1, v3)
        self.assertEqual(v0 + v2, v4)

    def test_sub(self):
        v0 = Vec(12, 34)
        v1 = Vec(56, 78)
        v2 = Vec(-910, -1112)
        v3 = Vec(12 - 56, 34 - 78)
        v4 = Vec(12 + 910, 34 + 1112)
        self.assertEqual(v0 - v1, v3)
        self.assertEqual(v0 - v2, v4)

    def test_mul(self):
        v0 = Vec(12, 34)
        K  = 3.5
        v1 = Vec(12*K, 34*K)
        self.assertEqual(v0*K, v1)
        self.assertEqual(K*v0, v1)

    def test_div(self):
        v0 = Vec(12, 34)
        K  = 2
        v1 = Vec(12/K, 34/K)
        self.assertEqual(v0/K, v1)

    def test_neg(self):
        v0 = Vec(12, 34)
        v1 = Vec(-12, -34)
        self.assertEqual(-v0, v1)

    def test_pos(self):
        v0 = Vec(12, 34)
        self.assertEqual(+v0, v0)

    def test_abs(self):
        v0 = Vec(3, 4)
        self.assertEqual(abs(v0), 5)

    def test_from_rect(self):
        v0 = Vec.from_rect(12, 34)
        v1 = Vec(12, 34)
        self.assertEqual(v0, v1)

    def test_from_polar(self):
        v0 = Vec.from_polar(5, math.atan2(3, 4))
        v1 = Vec(4, 3)
        self.assertEqual(v0, v1)

    def test_arg(self):
        v0 = Vec(1, 1)
        self.assertEqual(v0.arg(), math.pi / 4)

    def test_norm_squared(self):
        v0 = Vec(3, 4)
        self.assertEqual(v0.norm_squared(), 25)

    def test_norm(self):
        v0 = Vec(3, 4)
        self.assertEqual(v0.norm(), 5)

    def test_dot(self):
        v0 = Vec(12, 34)
        v1 = Vec(56, 78)
        self.assertEqual(v0.dot(v1), 12*56 + 34*78)
        self.assertEqual(v1.dot(v0), 56*12 + 78*34)

    def test_perpendicular(self):
        v0 = Vec(2, 1)
        v1 = Vec(-1, 2)
        self.assertEqual(v0.perpendicular(), v1)
        self.assertEqual(v0.dot(v1), 0)

    def test_is_collinear(self):
        v0 = Vec(0, 0)
        v1 = Vec(1, 2)
        v2 = Vec(2, 1)
        v3 = Vec(4, 8)
        v4 = Vec(-5, -10)
        v5 = Vec(12, 6)
        self.assertTrue(v0.is_collinear(v0))
        self.assertTrue(v0.is_collinear(v1))
        self.assertTrue(v0.is_collinear(v2))
        self.assertTrue(v0.is_collinear(v3))
        self.assertTrue(v0.is_collinear(v4))
        self.assertTrue(v0.is_collinear(v5))

        self.assertTrue(v1.is_collinear(v0))
        self.assertTrue(v1.is_collinear(v1))
        self.assertFalse(v1.is_collinear(v2))
        self.assertTrue(v1.is_collinear(v3))
        self.assertTrue(v1.is_collinear(v4))
        self.assertFalse(v1.is_collinear(v5))

        self.assertTrue(v2.is_collinear(v0))
        self.assertFalse(v2.is_collinear(v1))
        self.assertTrue(v2.is_collinear(v2))
        self.assertFalse(v2.is_collinear(v3))
        self.assertFalse(v2.is_collinear(v4))
        self.assertTrue(v2.is_collinear(v5))

        self.assertTrue(v3.is_collinear(v0))
        self.assertTrue(v3.is_collinear(v1))
        self.assertFalse(v3.is_collinear(v2))
        self.assertTrue(v3.is_collinear(v3))
        self.assertTrue(v3.is_collinear(v4))
        self.assertFalse(v3.is_collinear(v5))

        self.assertTrue(v4.is_collinear(v0))
        self.assertTrue(v4.is_collinear(v1))
        self.assertFalse(v4.is_collinear(v2))
        self.assertTrue(v4.is_collinear(v3))
        self.assertTrue(v4.is_collinear(v4))
        self.assertFalse(v4.is_collinear(v5))

        self.assertTrue(v5.is_collinear(v0))
        self.assertFalse(v5.is_collinear(v1))
        self.assertTrue(v5.is_collinear(v2))
        self.assertFalse(v5.is_collinear(v3))
        self.assertFalse(v5.is_collinear(v4))
        self.assertTrue(v5.is_collinear(v5))

    def test_is_perpendicular(self):
        v0 = Vec(0, 0)
        v1 = Vec(1, 1)
        v2 = Vec(-5, 5)
        v3 = Vec(3, -3)
        v4 = Vec(1, 2)
        self.assertTrue(v0.is_perpendicular(v0))
        self.assertTrue(v0.is_perpendicular(v1))
        self.assertTrue(v0.is_perpendicular(v2))
        self.assertTrue(v0.is_perpendicular(v3))
        self.assertTrue(v0.is_perpendicular(v4))

        self.assertTrue(v1.is_perpendicular(v0))
        self.assertFalse(v1.is_perpendicular(v1))
        self.assertTrue(v1.is_perpendicular(v2))
        self.assertTrue(v1.is_perpendicular(v3))
        self.assertFalse(v1.is_perpendicular(v4))

        self.assertTrue(v2.is_perpendicular(v0))
        self.assertTrue(v2.is_perpendicular(v1))
        self.assertFalse(v2.is_perpendicular(v2))
        self.assertFalse(v2.is_perpendicular(v3))
        self.assertFalse(v2.is_perpendicular(v4))

        self.assertTrue(v3.is_perpendicular(v0))
        self.assertTrue(v3.is_perpendicular(v1))
        self.assertFalse(v3.is_perpendicular(v2))
        self.assertFalse(v3.is_perpendicular(v3))
        self.assertFalse(v3.is_perpendicular(v4))

        self.assertTrue(v4.is_perpendicular(v0))
        self.assertFalse(v4.is_perpendicular(v1))
        self.assertFalse(v4.is_perpendicular(v2))
        self.assertFalse(v4.is_perpendicular(v3))
        self.assertFalse(v4.is_perpendicular(v4))


if __name__ == '__main__':
    unittest.main()
