import unittest
import os
from scripts.combined_detection import combined_detection


class TestCombinedDetection(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

        self.x_path = os.path.join(base_dir, 'data', 'X_test_small.csv')
        self.y_path = os.path.join(base_dir, 'data', 'y_test_small.csv')
        self.output_path = os.path.join(base_dir, 'test_data', 'combined_detection_results_small_sample.csv')
        self.rf_model_path = os.path.join(base_dir, 'models', 'random_forest_small.pkl')
        self.xgb_model_path = os.path.join(base_dir, 'models', 'xgboost_small.pkl')
        self.anomaly_model_path = os.path.join(base_dir, 'models', 'isolation_forest_small.pkl')

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