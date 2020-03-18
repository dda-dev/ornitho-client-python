from unittest import TestCase

from ornitho import Detail


class TestDetail(TestCase):
    def test_str(self):
        detail = Detail(1, "U", "PULL")
        self.assertEqual("1-U-PULL", detail.__str__())
