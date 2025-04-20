import unittest
import os
from scripts.combined_detection import combined_detection


class TestCombinedDetection(unittest.TestCase):
    def setUp(self):
        self.x_path = "../test_data/X_test_small_sample.csv"
        self.y_path = "../test_data/y_test_small_sample.csv"
        self.output_path = "../test_data/combined_detection_results_small_sample.csv"

        self.rf_model_path = "../models/random_forest_small.pkl"
        self.xgb_model_path = "../models/xgboost_small.pkl"
        self.anomaly_model_path = "../models/isolation_forest.pkl"

    def test_combined_detection_with_real_data(self):
        accuracy = combined_detection(
            X_path=self.x_path,
            y_path=self.y_path,
            rf_model_path=self.rf_model_path,
            xgb_model_path=self.xgb_model_path,
            anomaly_model_path=self.anomaly_model_path,
            output_path=self.output_path
        )

        self.assertTrue(os.path.exists(self.output_path))
        self.assertIsInstance(accuracy, float)
        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)

if __name__ == '__main__':
    unittest.main()