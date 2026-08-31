import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix


class DecisionTreeManager:
    """Manages Decision Tree classifier training, explainability, and evaluation."""

    def __init__(self, max_depth: int = 4, min_samples_leaf: int = 3, criterion: str = "gini", random_state: int = 42):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.criterion = criterion
        self.random_state = random_state
        self.model = DecisionTreeClassifier(
            max_depth=self.max_depth,
            min_samples_leaf=self.min_samples_leaf,
            criterion=self.criterion,
            random_state=self.random_state
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
            raise ValueError("Decision Tree model has not been trained.")
        if isinstance(X, dict):
            X = pd.DataFrame([X])[self.feature_names]
        elif isinstance(X, pd.DataFrame):
            X = X[self.feature_names]
        return self.model.predict(X)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_trained:
            raise ValueError("Decision Tree model has not been trained.")
        if isinstance(X, dict):
            X = pd.DataFrame([X])[self.feature_names]
        elif isinstance(X, pd.DataFrame):
            X = X[self.feature_names]
        return self.model.predict_proba(X)

    def get_feature_importances(self) -> pd.DataFrame:
        if not self.is_trained:
            raise ValueError("Decision Tree model has not been trained.")
        
        importances = self.model.feature_importances_
        df_imp = pd.DataFrame({
            "Feature": self.feature_names,
            "Importance": importances,
            "Percentage": (importances / importances.sum()) * 100 if importances.sum() > 0 else 0
        })
        return df_imp.sort_values(by="Importance", ascending=False).reset_index(drop=True)

    def evaluate(self, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
        y_pred = self.predict(X_test)
        y_prob = self.predict_proba(X_test)[:, 1]

        return {
            "model_name": "Decision Tree",
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_prob),
            "confusion_matrix": confusion_matrix(y_test, y_pred),
            "y_true": y_test.values,
            "y_pred": y_pred,
            "y_prob": y_prob
        }

    def export_rules_vi(self) -> list:
        """Traverses the binary tree and converts nodes into human-readable decision rules."""
        if not self.is_trained:
            raise ValueError("Decision Tree model has not been trained.")

        tree_ = self.model.tree_
        feature_name = [
            self.feature_names[i] if i != -2 else "undefined!"
            for i in tree_.feature
        ]
        
        rules = []

        def recurse(node, current_rule):
            if tree_.feature[node] != -2:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                
                # Left branch (<= threshold)
                left_rule = current_rule.copy()
                left_rule.append(f"{name} ≤ {threshold:.2f}")
                recurse(tree_.children_left[node], left_rule)
                
                # Right branch (> threshold)
                right_rule = current_rule.copy()
                right_rule.append(f"{name} > {threshold:.2f}")
                recurse(tree_.children_right[node], right_rule)
            else:
                # Leaf node: compute class probability and support count
                samples = tree_.n_node_samples[node]
                values = tree_.value[node][0]
                total = values.sum()
                prob_fire = (values[1] / total) if total > 0 else 0
                predicted_class = "CHÁY RỪNG (Fire)" if prob_fire >= 0.5 else "AN TOÀN (Not Fire)"
                
                rule_text = " VÀ ".join(current_rule) if current_rule else "Tất cả trường hợp"
                rules.append({
                    "conditions": current_rule,
                    "condition_str": rule_text,
                    "prediction": predicted_class,
                    "fire_probability": prob_fire * 100,
                    "sample_count": int(samples),
                    "confidence": "Cao" if (prob_fire >= 0.85 or prob_fire <= 0.15) else "Trung bình"
                })

        recurse(0, [])
        return rules

    def plot_tree_diagram(self, figsize=(14, 7)):
        if not self.is_trained:
            raise ValueError("Decision Tree model has not been trained.")

        fig, ax = plt.subplots(figsize=figsize, dpi=120)
        plot_tree(
            self.model,
            feature_names=self.feature_names,
            class_names=["Not Fire", "Fire"],
            filled=True,
            rounded=True,
            fontsize=9,
            ax=ax,
            proportion=True
        )
        ax.set_title(f"Sơ đồ Phân Nhánh Cây Quyết Định (Decision Tree - Max Depth: {self.max_depth})", fontsize=12, fontweight="bold", pad=15)
        plt.tight_layout()
        return fig
