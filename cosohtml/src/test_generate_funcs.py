import unittest

from generate_funcs import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello world"
        self.assertEqual(extract_title(md), "Hello world")
    
    def test_extract_title_long(self):
        md = """
# Hello world
This is a paragraph
"""
        self.assertEqual(extract_title(md), "Hello world")

    def test_extract_title_none(self):
        md = """
## Hello world
This is a paragraph
"""
        with self.assertRaises(ValueError):
             extract_title(md)

if __name__ == "__main__":
    unittest.main()
