import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix


class RandomForestManager:
    """Manages Random Forest ensemble training, feature importances, and tree agreement analysis."""

    def __init__(self, n_estimators: int = 100, max_depth: int = 6, min_samples_leaf: int = 2, random_state: int = 42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state
        self.model = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            min_samples_leaf=self.min_samples_leaf,
            random_state=self.random_state,
            oob_score=True
        )
        self.feature_names = None
        self.is_trained = False

    def train(self, X: pd.DataFrame, y: pd.Series):
        self.feature_names = list(X.columns)
        self.model.fit(X, y)
        self.is_trained = True
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_trained:
            raise ValueError("Random Forest model has not been trained.")
        if isinstance(X, dict):
            X = pd.DataFrame([X])[self.feature_names]
        elif isinstance(X, pd.DataFrame):
            X = X[self.feature_names]
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_trained:
            raise ValueError("Random Forest model has not been trained.")
        if isinstance(X, dict):
            X = pd.DataFrame([X])[self.feature_names]
        elif isinstance(X, pd.DataFrame):
            X = X[self.feature_names]
        return self.model.predict_proba(X)

    def get_feature_importances(self) -> pd.DataFrame:
        if not self.is_trained:
            raise ValueError("Random Forest model has not been trained.")

        importances = self.model.feature_importances_
        std = np.std([tree.feature_importances_ for tree in self.model.estimators_], axis=0)

        df_imp = pd.DataFrame({
            "Feature": self.feature_names,
            "Importance": importances,
            "Percentage": (importances / importances.sum()) * 100 if importances.sum() > 0 else 0,
            "StdDev": std
        })
        return df_imp.sort_values(by="Importance", ascending=False).reset_index(drop=True)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        y_pred = self.predict(X_test)
        y_prob = self.predict_proba(X_test)[:, 1]

        return {
            "model_name": "Random Forest",
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_prob),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
            "oob_score": getattr(self.model, "oob_score_", None),
            "y_true": y_test.values,
            "y_pred": y_pred,
            "y_prob": y_prob
        }

    def get_tree_agreement(self, X_single: pd.DataFrame) -> dict:
        """Computes vote agreement ratio across individual trees for a single observation."""
        if not self.is_trained:
            raise ValueError("Random Forest model has not been trained.")
        if isinstance(X_single, dict):
            X_single = pd.DataFrame([X_single])[self.feature_names]
        elif isinstance(X_single, pd.DataFrame):
            X_single = X_single[self.feature_names]

        tree_preds = [tree.predict(X_single.values)[0] for tree in self.model.estimators_]
        fire_votes = sum(tree_preds)
        not_fire_votes = len(tree_preds) - fire_votes
        agreement_ratio = max(fire_votes, not_fire_votes) / len(tree_preds)

        return {
            "total_trees": len(self.model.estimators_),
            "fire_votes": fire_votes,
            "not_fire_votes": not_fire_votes,
            "agreement_ratio": agreement_ratio * 100
        }
