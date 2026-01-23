from unittest import TestCase

from ornitho import Detail


class TestDetail(TestCase):
    def test_str(self):
        detail = Detail(1, "U", "PULL")
        self.assertEqual("None-1-U-PULL", detail.__str__())

    def test_excel_str_german(self):
        details = [
            Detail(2, "M", "U"),
            Detail(3, "M", "PULL"),
            Detail(4, "F", "1Y"),
            Detail(5, "FT", "2Y"),
            Detail(6, "U", "3Y"),
            Detail(7, "M", "4Y"),
            Detail(8, "F", "5Y"),
            Detail(9, "FT", "IMM"),
            Detail(10, "M", "AD"),
        ]
        self.assertEqual(
            "2x Männchen / 3x Männchen Pulli / nicht-flügge / 4x Weibchen 1. KJ / diesjährige / 5x weibchenfarbige 2. KJ / vorjährige / 6x 3. KJ / 7x Männchen 4. KJ / 8x Weibchen 5. KJ / 9x weibchenfarbige immature / 10x Männchen adulte",
            Detail.list_to_excel_str(details),
        )

        details = [
            Detail(1, "U", "PULL"),
            Detail(1, "M", "U"),
            Detail(1, "F", "1Y"),
            Detail(1, "FT", "2Y"),
            Detail(1, "U", "3Y"),
            Detail(1, "M", "4Y"),
            Detail(1, "F", "5Y"),
            Detail(1, "FT", "IMM"),
            Detail(1, "M", "AD"),
        ]
        self.assertEqual(
            "1x Pullus / nicht-flügge / 1x Männchen / 1x Weibchen 1. KJ / diesjährig / 1x weibchenfarbig 2. KJ / vorjährig / 1x 3. KJ / 1x Männchen 4. KJ / 1x Weibchen 5. KJ / 1x weibchenfarbig immatur / 1x Männchen adult",
            Detail.list_to_excel_str(details),
        )
