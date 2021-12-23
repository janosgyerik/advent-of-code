import unittest

import utils


class TestUtils(unittest.TestCase):
    def test_lines_to_int_tuples(self):
        lines = [
            '194,556 -> 739,556',
            '818,920 -> 818,524',
            '340,734 -> 774,300',
        ]
        int_tuples = [
            [194, 556, 739, 556],
            [818, 920, 818, 524],
            [340, 734, 774, 300],
        ]
        self.assertEqual(utils.strings_to_int_lists(lines), int_tuples)

    def test_whitespace_delimited_strings_to_lists(self):
        lines = [
            'yb start',
            'de   vd',
            'rj      yb',
        ]
        expected = [
            ['yb', 'start'],
            ['de', 'vd'],
            ['rj', 'yb'],
        ]
        self.assertEqual(utils.delimited_strings_to_lists(lines), expected)

    def test_hyphen_delimited_strings_to_lists(self):
        lines = [
            'yb-start',
            'de-vd',
            'rj-yb',
        ]
        expected = [
            ['yb', 'start'],
            ['de', 'vd'],
            ['rj', 'yb'],
        ]
        self.assertEqual(utils.delimited_strings_to_lists(lines, delim='-'), expected)

    def test_extract_all_valid_ints(self):
        line = 'target area: x=96..125, y=-144..-98'
        self.assertEqual(utils.extract_all_valid_ints(line), [96, 125, -144, -98])


class TestPriorityQueue(unittest.TestCase):
    def test_random_order_items_are_returned_in_priority_order(self):
        pq = utils.PriorityQueue()
        pq.add_or_update(1, 10)
        pq.add_or_update(2, 5)
        pq.add_or_update(3, 15)

        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 1)
        self.assertEqual(pq.pop(), 3)

    def test_ordered_items_are_returned_in_priority_order(self):
        pq = utils.PriorityQueue()
        pq.add_or_update(1, 11)
        pq.add_or_update(2, 12)
        pq.add_or_update(3, 13)

        self.assertEqual(pq.pop(), 1)
        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 3)

    def test_reverse_ordered_items_are_returned_in_priority_order(self):
        pq = utils.PriorityQueue()
        pq.add_or_update(1, 13)
        pq.add_or_update(2, 12)
        pq.add_or_update(3, 11)

        self.assertEqual(pq.pop(), 3)
        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 1)

    def test_returns_items_in_correct_order_after_priority_change(self):
        pq = utils.PriorityQueue()
        pq.add_or_update(1, 11)
        pq.add_or_update(2, 12)
        pq.add_or_update(3, 13)

        pq.add_or_update(2, 5)

        self.assertEqual(pq.pop(), 2)
        self.assertEqual(pq.pop(), 1)
        self.assertEqual(pq.pop(), 3)

    def test_returns_items_in_correct_order_after_removal(self):
        pq = utils.PriorityQueue()
        pq.add_or_update(1, 11)
        pq.add_or_update(2, 12)
        pq.add_or_update(3, 13)

        pq.remove(2)

        self.assertEqual(pq.pop(), 1)
        self.assertEqual(pq.pop(), 3)

    def test_pop_empty_raises_KeyError(self):
        pq = utils.PriorityQueue()
        self.assertRaises(KeyError, lambda: pq.pop())

    def test_remove_nonexistent_raises_KeyError(self):
        pq = utils.PriorityQueue()
        pq.add_or_update(1, 1)
        self.assertRaises(KeyError, lambda: pq.remove(2))


if __name__ == '__main__':
    unittest.main()
