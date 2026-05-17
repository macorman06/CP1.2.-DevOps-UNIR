import unittest
import pytest
from unittest.mock import patch
import http.client

from app.api import hello, add, substract


@pytest.mark.unit
class TestApi(unittest.TestCase):

    def test_hello_returns_message(self):
        result = hello()
        self.assertIn("Hello from The Calculator!\n", result)

    @patch('app.api.util.convert_to_number')
    @patch('app.api.CALCULATOR.add')
    def test_add_returns_correct_result(self, mock_add, mock_convert):
        mock_convert.side_effect = [2, 3]
        mock_add.return_value = 5
        result, status, _ = add("2", "3")
        self.assertEqual("5", result)
        self.assertEqual(http.client.OK, status)

    @patch('app.api.util.convert_to_number')
    def test_add_fails_with_invalid_parameter(self, mock_convert):
        mock_convert.side_effect = TypeError("Operator cannot be converted to number")
        result, status, _ = add("x", "3")
        self.assertEqual(http.client.BAD_REQUEST, status)

    @patch('app.api.util.convert_to_number')
    @patch('app.api.CALCULATOR.substract')
    def test_substract_returns_correct_result(self, mock_sub, mock_convert):
        mock_convert.side_effect = [10, 3]
        mock_sub.return_value = 7
        result, status, _ = substract("10", "3")
        self.assertEqual("7", result)
        self.assertEqual(http.client.OK, status)

    @patch('app.api.util.convert_to_number')
    def test_substract_fails_with_invalid_parameter(self, mock_convert):
        mock_convert.side_effect = TypeError("Operator cannot be converted to number")
        result, status, _ = substract("10", "x")
        self.assertEqual(http.client.BAD_REQUEST, status)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()