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
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )

        self.dt_manager.train(self.X_train, self.y_train)
        self.rf_manager.train(self.X_train, self.y_train)

        self.dt_eval = self.dt_manager.evaluate(self.X_test, self.y_test)
        self.rf_eval = self.rf_manager.evaluate(self.X_test, self.y_test)

        self.metrics_summary = pd.DataFrame([
            {
                "Thuật toán": "Decision Tree",
                "Độ chính xác (Accuracy)": f"{self.dt_eval['accuracy'] * 100:.2f}%",
                "Độ chuẩn xác (Precision)": f"{self.dt_eval['precision'] * 100:.2f}%",
                "Độ bao phủ (Recall)": f"{self.dt_eval['recall'] * 100:.2f}%",
                "Điểm F1 (F1-Score)": f"{self.dt_eval['f1'] * 100:.2f}%",
                "Chỉ số ROC-AUC": f"{self.dt_eval['roc_auc']:.4f}",
                "Đặc tính": "Mô hình quy tắc trực giao, diễn giải tường minh",
            },
            {
                "Thuật toán": "Random Forest",
                "Độ chính xác (Accuracy)": f"{self.rf_eval['accuracy'] * 100:.2f}%",
                "Độ chuẩn xác (Precision)": f"{self.rf_eval['precision'] * 100:.2f}%",
                "Độ bao phủ (Recall)": f"{self.rf_eval['recall'] * 100:.2f}%",
                "Điểm F1 (F1-Score)": f"{self.rf_eval['f1'] * 100:.2f}%",
                "Chỉ số ROC-AUC": f"{self.rf_eval['roc_auc']:.4f}",
                "Đặc tính": "Mô hình tổ hợp bagging, giảm phương sai, chống nhiễu",
            }
        ])
        return self

    def plot_confusion_matrices_plotly(self, palette: dict = None):
        if self.dt_eval is None or self.rf_eval is None:
            raise ValueError("Models must be evaluated before plotting confusion matrices.")

        paper_bg = palette["chart_paper"] if palette else "#ffffff"
        plot_bg = palette["chart_plot"] if palette else "#ffffff"
        text_color = palette["chart_text"] if palette else "#090d16"
        grid_color = palette["chart_grid"] if palette else "#e2e8f0"
        is_dark = palette.get("is_dark", False) if palette else False

        cm_dt = self.dt_eval["confusion_matrix"]
        cm_rf = self.rf_eval["confusion_matrix"]
        labels = ["Không cháy (0)", "Cháy (1)"]

        if is_dark:
            neutral_scale = [
                [0.0, "#131b2e"],
                [0.35, "#1e293b"],
                [0.7, "#334155"],
                [1.0, "#38bdf8"]
            ]
        else:
            neutral_scale = [
                [0.0, "#f8fafc"],
                [0.35, "#cbd5e1"],
                [0.7, "#64748b"],
                [1.0, "#090d16"]
            ]

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
                colorscale=neutral_scale, text=cm_dt,
                texttemplate="%{text}", textfont={"size": 15, "family": "Consolas, monospace", "color": text_color},
                showscale=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Heatmap(
                z=cm_rf, x=labels, y=labels,
                colorscale=neutral_scale, text=cm_rf,
                texttemplate="%{text}", textfont={"size": 15, "family": "Consolas, monospace", "color": text_color},
                showscale=False
            ),
            row=1, col=2
        )

        fig.update_xaxes(title_text="Giá trị dự đoán", row=1, col=1, gridcolor=grid_color, title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig.update_xaxes(title_text="Giá trị dự đoán", row=1, col=2, gridcolor=grid_color, title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig.update_yaxes(title_text="Giá trị thực tế", row=1, col=1, gridcolor=grid_color, title_font=dict(color=text_color), tickfont=dict(color=text_color))
        fig.update_yaxes(title_text="Giá trị thực tế", row=1, col=2, gridcolor=grid_color, title_font=dict(color=text_color), tickfont=dict(color=text_color))

        fig.update_layout(
            title={"text": "Ma Trận Nhầm Lẫn (Confusion Matrix)", "font": {"size": 14, "color": text_color}},
            height=360,
            paper_bgcolor=paper_bg,
            plot_bgcolor=plot_bg,
            font={"family": "Segoe UI, Arial, sans-serif", "color": text_color, "size": 12},
            margin=dict(l=30, r=30, t=50, b=30)
        )
        return fig

    def plot_roc_curves_plotly(self, palette: dict = None):
        if self.dt_eval is None or self.rf_eval is None:
            raise ValueError("Models must be evaluated before plotting ROC curves.")

        paper_bg = palette["chart_paper"] if palette else "#ffffff"
        plot_bg = palette["chart_plot"] if palette else "#ffffff"
        text_color = palette["chart_text"] if palette else "#090d16"
        grid_color = palette["chart_grid"] if palette else "#e2e8f0"
        is_dark = palette.get("is_dark", False) if palette else False

        y_true = self.y_test.values
        fpr_dt, tpr_dt, _ = roc_curve(y_true, self.dt_eval["y_prob"])
        fpr_rf, tpr_rf, _ = roc_curve(y_true, self.rf_eval["y_prob"])

        rf_color = "#38bdf8" if is_dark else "#090d16"
        dt_color = "#94a3b8" if is_dark else "#475569"
        base_color = "#475569" if is_dark else "#cbd5e1"
        legend_bg = "rgba(19, 27, 46, 0.9)" if is_dark else "rgba(255,255,255,0.9)"

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fpr_dt, y=tpr_dt, mode="lines",
            name=f"Decision Tree (AUC: {self.dt_eval['roc_auc']:.3f})",
            line=dict(color=dt_color, width=2)
        ))
        fig.add_trace(go.Scatter(
            x=fpr_rf, y=tpr_rf, mode="lines",
            name=f"Random Forest (AUC: {self.rf_eval['roc_auc']:.3f})",
            line=dict(color=rf_color, width=2.5)
        ))
        fig.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines",
            name="Baseline ngẫu nhiên (0.50)",
            line=dict(color=base_color, width=1.5, dash="dash")
        ))

        fig.update_layout(
            title={"text": "Đường Cong ROC (Receiver Operating Characteristic)", "font": {"size": 14, "color": text_color}},
            xaxis=dict(title=dict(text="False Positive Rate", font=dict(color=text_color)), gridcolor=grid_color, zeroline=False, tickfont=dict(color=text_color)),
            yaxis=dict(title=dict(text="True Positive Rate", font=dict(color=text_color)), gridcolor=grid_color, zeroline=False, tickfont=dict(color=text_color)),
            height=360,
            paper_bgcolor=paper_bg,
            plot_bgcolor=plot_bg,
            font={"family": "Segoe UI, Arial, sans-serif", "color": text_color, "size": 12},
            hovermode="x unified",
            legend=dict(yanchor="bottom", y=0.06, xanchor="right", x=0.96, bgcolor=legend_bg, font=dict(color=text_color)),
            margin=dict(l=30, r=30, t=50, b=30)
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
