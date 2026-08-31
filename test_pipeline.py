import sys
import os
import unittest
import pandas as pd
import numpy as np

# Ensure proper console encoding on Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from data_loader import load_and_clean_data, get_feature_data
from models import DecisionTreeManager, RandomForestManager, ModelEvaluator
from config import ALL_MODEL_FEATURES, RISK_LEVELS


class TestForestFirePipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.df = load_and_clean_data()
        cls.X, cls.y = get_feature_data(cls.df)

    def test_data_integrity(self):
        self.assertEqual(len(self.df), 244, "Dataset must have exactly 244 observations.")
        self.assertFalse(self.df[ALL_MODEL_FEATURES].isnull().any().any(), "Features must not contain NaN values.")
        self.assertTrue(set(self.df["Region"].unique()) == {"Bejaia", "Sidi-Bel Abbes"}, "Must contain both regions.")
        self.assertTrue(set(self.df["Fire_Label"].unique()) == {0, 1}, "Labels must be binary 0 and 1.")

    def test_decision_tree_module(self):
        dt = DecisionTreeManager(max_depth=4, random_state=42)
        dt.train(self.X, self.y)
        self.assertTrue(dt.is_trained)

        preds = dt.predict(self.X)
        self.assertEqual(len(preds), len(self.y))
        
        df_imp = dt.get_feature_importances()
        self.assertGreater(len(df_imp), 0)
        self.assertAlmostEqual(df_imp["Percentage"].sum(), 100.0, places=1)

        rules = dt.export_rules_vi()
        self.assertGreater(len(rules), 0)
        self.assertIn("conditions", rules[0])

    def test_random_forest_module(self):
        rf = RandomForestManager(n_estimators=50, max_depth=5, random_state=42)
        rf.train(self.X, self.y)
        self.assertTrue(rf.is_trained)

        probs = rf.predict_proba(self.X)
        self.assertEqual(probs.shape, (len(self.X), 2))

        single_sample = self.X.iloc[[0]]
        agreement = rf.get_tree_agreement(single_sample)
        self.assertEqual(agreement["total_trees"], 50)
        self.assertEqual(agreement["fire_votes"] + agreement["not_fire_votes"], 50)

    def test_model_evaluator(self):
        evaluator = ModelEvaluator(test_size=0.2, random_state=42)
        evaluator.fit_and_evaluate(self.X, self.y)

        self.assertIsNotNone(evaluator.metrics_summary)
        self.assertGreaterEqual(evaluator.dt_eval["accuracy"], 0.85)
        self.assertGreaterEqual(evaluator.rf_eval["accuracy"], 0.85)

        df_comp = evaluator.get_comparison_feature_importances()
        self.assertEqual(len(df_comp), len(ALL_MODEL_FEATURES))

    def test_extreme_inference_scenarios(self):
        rf = RandomForestManager(n_estimators=50, random_state=42)
        rf.train(self.X, self.y)

        # High precipitation and extreme humidity should yield negligible fire probability
        rainy_day = pd.DataFrame([{
            "Temperature": 18.0, "RH": 95.0, "Ws": 15.0, "Rain": 20.0,
            "FFMC": 30.0, "DMC": 2.0, "DC": 10.0, "ISI": 0.1, "BUI": 2.0, "FWI": 0.0
        }])[ALL_MODEL_FEATURES]
        rain_prob = rf.predict_proba(rainy_day)[0][1]
        self.assertLess(rain_prob, 0.20)

        # Extreme heatwave and high FFMC/ISI should yield high fire probability
        inferno_day = pd.DataFrame([{
            "Temperature": 42.0, "RH": 22.0, "Ws": 25.0, "Rain": 0.0,
            "FFMC": 95.0, "DMC": 50.0, "DC": 180.0, "ISI": 15.0, "BUI": 55.0, "FWI": 28.0
        }])[ALL_MODEL_FEATURES]
        inferno_prob = rf.predict_proba(inferno_day)[0][1]
        self.assertGreater(inferno_prob, 0.80)


if __name__ == "__main__":
    unittest.main()
