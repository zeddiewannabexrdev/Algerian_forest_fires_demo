import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve

from .decision_tree_model import DecisionTreeManager
from .random_forest_model import RandomForestManager


class ModelEvaluator:
    """Provides comparative benchmarking, ROC curves, and confusion matrices for both models."""

    def __init__(self, test_size: float = 0.2, random_state: int = 42):
        self.test_size = test_size
        self.random_state = random_state
        self.dt_manager = DecisionTreeManager(random_state=random_state)
        self.rf_manager = RandomForestManager(random_state=random_state)
        self.metrics_summary = None
        self.dt_eval = None
        self.rf_eval = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def fit_and_evaluate(self, X: pd.DataFrame, y: pd.Series):
        # Stratified train/test split to preserve class distribution
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )

        self.dt_manager.train(self.X_train, self.y_train)
        self.rf_manager.train(self.X_train, self.y_train)

        self.dt_eval = self.dt_manager.evaluate(self.X_test, self.y_test)
        self.rf_eval = self.rf_manager.evaluate(self.X_test, self.y_test)

        self.metrics_summary = pd.DataFrame([
            {
                "Thuật toán": "Cây Quyết Định (Decision Tree)",
                "Độ chính xác (Accuracy)": f"{self.dt_eval['accuracy'] * 100:.2f}%",
                "Độ chuẩn xác (Precision)": f"{self.dt_eval['precision'] * 100:.2f}%",
                "Độ bao phủ (Recall)": f"{self.dt_eval['recall'] * 100:.2f}%",
                "Điểm F1 (F1-Score)": f"{self.dt_eval['f1'] * 100:.2f}%",
                "Chỉ số ROC-AUC": f"{self.dt_eval['roc_auc']:.4f}",
                "Ưu điểm nổi bật": "Diễn giải trực quan 100%, xuất luật If-Else rõ ràng",
            },
            {
                "Thuật toán": "Rừng Ngẫu Nhiên (Random Forest)",
                "Độ chính xác (Accuracy)": f"{self.rf_eval['accuracy'] * 100:.2f}%",
                "Độ chuẩn xác (Precision)": f"{self.rf_eval['precision'] * 100:.2f}%",
                "Độ bao phủ (Recall)": f"{self.rf_eval['recall'] * 100:.2f}%",
                "Điểm F1 (F1-Score)": f"{self.rf_eval['f1'] * 100:.2f}%",
                "Chỉ số ROC-AUC": f"{self.rf_eval['roc_auc']:.4f}",
                "Ưu điểm nổi bật": "Độ chính xác cao, bền vững với nhiễu, khử quá khớp",
            }
        ])
        return self

    def plot_confusion_matrices_plotly(self):
        if self.dt_eval is None or self.rf_eval is None:
            raise ValueError("Models must be evaluated before plotting confusion matrices.")

        cm_dt = self.dt_eval["confusion_matrix"]
        cm_rf = self.rf_eval["confusion_matrix"]
        labels = ["Không cháy (0)", "Cháy (1)"]

        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=(
                f"Decision Tree (Acc: {self.dt_eval['accuracy']*100:.1f}%)",
                f"Random Forest (Acc: {self.rf_eval['accuracy']*100:.1f}%)"
            ),
            horizontal_spacing=0.15
        )

        fig.add_trace(
            go.Heatmap(
                z=cm_dt, x=labels, y=labels,
                colorscale="Blues", text=cm_dt,
                texttemplate="%{text}", textfont={"size": 16},
                showscale=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Heatmap(
                z=cm_rf, x=labels, y=labels,
                colorscale="Greens", text=cm_rf,
                texttemplate="%{text}", textfont={"size": 16},
                showscale=False
            ),
            row=1, col=2
        )

        fig.update_xaxes(title_text="Dự đoán của mô hình", row=1, col=1)
        fig.update_xaxes(title_text="Dự đoán của mô hình", row=1, col=2)
        fig.update_yaxes(title_text="Thực tế kiểm sát", row=1, col=1)
        fig.update_yaxes(title_text="Thực tế kiểm sát", row=1, col=2)

        fig.update_layout(
            title="Đối Chiếu Ma Trận Nhầm Lẫn (Confusion Matrix)",
            height=400,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig

    def plot_roc_curves_plotly(self):
        if self.dt_eval is None or self.rf_eval is None:
            raise ValueError("Models must be evaluated before plotting ROC curves.")

        y_true = self.y_test.values
        fpr_dt, tpr_dt, _ = roc_curve(y_true, self.dt_eval["y_prob"])
        fpr_rf, tpr_rf, _ = roc_curve(y_true, self.rf_eval["y_prob"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fpr_dt, y=tpr_dt, mode="lines+markers",
            name=f"Decision Tree (AUC = {self.dt_eval['roc_auc']:.3f})",
            line=dict(color="#3b82f6", width=2.5)
        ))
        fig.add_trace(go.Scatter(
            x=fpr_rf, y=tpr_rf, mode="lines+markers",
            name=f"Random Forest (AUC = {self.rf_eval['roc_auc']:.3f})",
            line=dict(color="#10b981", width=3)
        ))
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines",
            name="Baseline (AUC = 0.5)",
            line=dict(color="#9ca3af", dash="dash")
        ))

        fig.update_layout(
            title="Đường Cong ROC (Receiver Operating Characteristic)",
            xaxis_title="Tỷ lệ Dương tính Giả (False Positive Rate)",
            yaxis_title="Tỷ lệ Dương tính Thật (True Positive Rate / Recall)",
            height=430,
            hovermode="x unified",
            legend=dict(yanchor="bottom", y=0.05, xanchor="right", x=0.98),
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig

    def get_comparison_feature_importances(self) -> pd.DataFrame:
        df_dt = self.dt_manager.get_feature_importances()[["Feature", "Percentage"]].rename(
            columns={"Percentage": "DT_Percentage"}
        )
        df_rf = self.rf_manager.get_feature_importances()[["Feature", "Percentage"]].rename(
            columns={"Percentage": "RF_Percentage"}
        )
        merged = pd.merge(df_rf, df_dt, on="Feature")
        merged["Chênh lệch (RF - DT)"] = merged["RF_Percentage"] - merged["DT_Percentage"]
        return merged.sort_values(by="RF_Percentage", ascending=False).reset_index(drop=True)
