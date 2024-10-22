import unittest
from app.services.clo_extractor import extract_clos_from_excel

class TestCLOExtractor(unittest.TestCase):

    def test_extract_clos(self):
        sample_data = 'path/to/sample_data.xlsx'
        clos = extract_clos_from_excel(sample_data)
        self.assertGreater(len(clos), 0)  # Test if CLOs are extracted

if __name__ == '__main__':
    unittest.main()
