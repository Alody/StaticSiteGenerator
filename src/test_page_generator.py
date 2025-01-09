import unittest
from page_generator import extract_title

class TestExtractTitle(unittest.TestCase):

    def test_extract_title_valid(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_extract_title_no_h1(self):
        markdown = "## Not an H1 header"
        with self.assertRaises(ValueError):
            extract_title(markdown)
    
    def test_extract_title_multiple_h1(self):
        markdown = "# First Title\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

if __name__ == "__main__":
    unittest.main()
