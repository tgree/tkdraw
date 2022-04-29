import unittest

from .. import Vec, Rect, LineSegment, Line


class TestRect(unittest.TestCase):
    def test_params(self):
        r = Rect(Vec(1, 2), Vec(-5, 3))
        self.assertEqual(r.width, 6)
        self.assertEqual(r.height, 1)
        self.assertIn(LineSegment(Vec(1, 2), Vec(1, 3)), r.segments)
        self.assertIn(LineSegment(Vec(1, 2), Vec(-5, 2)), r.segments)
        self.assertIn(LineSegment(Vec(-5, 3), Vec(-5, 2)), r.segments)
        self.assertIn(LineSegment(Vec(-5, 3), Vec(1, 3)), r.segments)

    def test_line_intersection_ts(self):
        # 2 wide x 1 high
        r = Rect(Vec(1, 1), Vec(3, 2))
        ts = r.line_intersection_ts(Line(Vec(0, 1.5), Vec(4, 1.5)))
        self.assertEqual(len(ts), 2)
        self.assertIn(0.25, ts)
        self.assertIn(0.75, ts)

        ts = r.line_intersection_ts(Line(Vec(0, 1), Vec(4, 1)))
        self.assertEqual(len(ts), 2)
        self.assertIn(0.25, ts)
        self.assertIn(0.75, ts)

        ts = r.line_intersection_ts(Line(Vec(0, 2), Vec(2, 0)))
        self.assertEqual(ts, [0.5, 0.5])

        ts = r.line_intersection_ts(Line(Vec(-1, 3), Vec(1, 2)))
        self.assertEqual(sorted(ts), [1, 1, 2, 2])

        ts = r.line_intersection_ts(Line(Vec(1, 2), Vec(3, 1)))
        self.assertEqual(sorted(ts), [0, 0, 1, 1])

        ts = r.line_intersection_ts(Line(Vec(3, 2), Vec(1, 1)))
        self.assertEqual(sorted(ts), [0, 0, 1, 1])

        ts = r.line_intersection_ts(Line(Vec(0, 10), Vec(10, 10)))
        self.assertEqual(ts, [])

        ts = r.line_intersection_ts(Line(Vec(-1, 1.5), Vec(0, 1.5)))
        self.assertEqual(sorted(ts), [2, 4])

    def test_overlaps_segment(self):
        # 2 wide x 1 high
        r = Rect(Vec(1, 1), Vec(3, 2))
        self.assertTrue(r.overlaps_segment(LineSegment(
            Vec(0, 1.5), Vec(4, 1.5))))
        self.assertTrue(r.overlaps_segment(LineSegment(Vec(0, 1), Vec(4, 1))))
        self.assertTrue(r.overlaps_segment(LineSegment(Vec(0, 2), Vec(2, 0))))
        self.assertTrue(r.overlaps_segment(LineSegment(Vec(-1, 3), Vec(1, 2))))
        self.assertTrue(r.overlaps_segment(LineSegment(Vec(1, 2), Vec(3, 1))))
        self.assertTrue(r.overlaps_segment(LineSegment(Vec(3, 2), Vec(1, 1))))
        self.assertFalse(r.overlaps_segment(LineSegment(
            Vec(0, 10), Vec(10, 10))))
        self.assertFalse(r.overlaps_segment(LineSegment(
            Vec(-1, 1.5), Vec(0, 1.5))))
        self.assertTrue(r.overlaps_segment(LineSegment(
            Vec(1.5, 1.5), Vec(2.5, 1.5))))
        self.assertTrue(r.overlaps_segment(LineSegment(
            Vec(3, 2), Vec(4, 4))))
        self.assertTrue(r.overlaps_segment(LineSegment(
            Vec(4, 4), Vec(3, 2))))


if __name__ == '__main__':
    unittest.main()
