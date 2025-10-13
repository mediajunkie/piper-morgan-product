"""
Simple test example to verify unittest functionality
"""

import unittest


class TestSimpleExample(unittest.TestCase):
    """Simple test class to verify unittest works"""

    def test_basic_assertion(self):
        """Test that basic assertions work"""
        self.assertEqual(2 + 2, 4)
        self.assertTrue(True)
        self.assertFalse(False)

    def test_string_operations(self):
        """Test string operations"""
        test_string = "hello world"
        self.assertIn("hello", test_string)
        self.assertEqual(len(test_string), 11)


if __name__ == "__main__":
    unittest.main()
