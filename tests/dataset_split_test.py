import unittest
import os
from scripts.dataset_split import split_dataset


class TestDatasetSplit(unittest.TestCase):
    def setUp(self):
        # using relative path as it is different for test
        self.sample_csv_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'test_data', 'sample.csv')
        )
    def test_dataset_split_creates_outputs_in_test_data(self):
        """Run split_dataset on sample.csv and check that the split files are saved to test_data folder."""

        split_dataset(self.sample_csv_path, small_size=100, output_dir='../test_data')

        expected_files = [
            "X_train_small.csv",
            "X_test_small.csv",
            "y_train_small.csv",
            "y_test_small.csv"
        ]

        for filename in expected_files:
            full_path = os.path.join('../test_data', filename)
            self.assertTrue(os.path.exists(full_path), f"{filename} was not created.")


if __name__ == '__main__':
    unittest.main()