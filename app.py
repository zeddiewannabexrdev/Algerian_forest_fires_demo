import streamlit as st
import pandas as pd
import numpy as np

from data_loader import load_and_clean_data, get_feature_data
from models import ModelEvaluator
from views import (
    render_alert_view,
    render_climate_view,
    render_regional_view,
    render_seasonal_view,
    render_explainability_view
)

# Page configuration
st.set_page_config(
    page_title="Giám Sát & Cảnh Báo Cháy Rừng Algeria",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling for dashboard cards and tabs
st.markdown("""
<style>
    .stSlider > div { padding-top: 10px; }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 18px;
        border-radius: 6px 6px 0px 0px;
        font-weight: 600;
    }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Đang khởi tạo và huấn luyện 2 thuật toán Machine Learning...")
def init_models_and_evaluator(df: pd.DataFrame):
    X, y = get_feature_data(df)
    evaluator = ModelEvaluator(test_size=0.2, random_state=42)
    evaluator.fit_and_evaluate(X, y)
    return evaluator


def main():
    with st.spinner("Đang nạp và kiểm định tệp dữ liệu..."):
        df = load_and_clean_data()

    evaluator = init_models_and_evaluator(df)
    dt_model = evaluator.dt_manager
    rf_model = evaluator.rf_manager

    with st.sidebar:
        st.markdown("## 🔥 Trung Tâm Giám Sát Lâm Nghiệp")
        st.caption("Ứng dụng phân tích dữ liệu & dự báo nguy cơ cháy rừng Algeria bằng AI")
        st.markdown("---")

        st.markdown("### 📊 Thống Kê Cơ Sở Dữ Liệu")
        total_samples = len(df)
        fire_samples = int(df["Fire_Label"].sum())
        safe_samples = total_samples - fire_samples

        st.write(f"• **Tổng số ngày quan trắc:** `{total_samples}`")
        st.write(f"• **Số ngày bùng phát cháy:** `{fire_samples}` ({fire_samples/total_samples*100:.1f}%)")
        st.write(f"• **Số ngày an toàn:** `{safe_samples}` ({safe_samples/total_samples*100:.1f}%)")
        st.write(f"• **Vùng Bejaia:** `122 ngày` (Duyên hải)")
        st.write(f"• **Vùng Sidi-Bel Abbes:** `122 ngày` (Nội địa)")

        st.markdown("---")
        st.markdown("### 🤖 Thông Số Mô Hình AI")
        st.write(f"• **Decision Tree Acc:** `{evaluator.dt_eval['accuracy']*100:.1f}%`")
        st.write(f"• **Random Forest Acc:** `{evaluator.rf_eval['accuracy']*100:.1f}%`")
        st.write(f"• **Tập kiểm tra (Test):** `20% (Stratified)`")

        st.markdown("---")
        st.markdown("### 🛠️ Kiến Trúc Module Độc Lập")
        st.caption("Các tệp thành phần riêng biệt:")
        st.code("""
data/
└── Algerian_forest_fires_dataset_UPDATE.csv
models/
├── decision_tree_model.py
├── random_forest_model.py
└── model_evaluator.py
views/
├── alert_view.py
├── climate_view.py
├── regional_view.py
├── seasonal_view.py
└── explainability_view.py
        """, language="text")

    st.title("🔥 Hệ Thống Cảnh Báo Sớm & Phân Tích Cháy Rừng Algeria")
    st.markdown("##### *Trung tâm điều hành hỗ trợ ra quyết định phòng chống cháy rừng tích hợp Trí Tuệ Nhân Tạo*")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🚨 Cảnh Báo Tức Thời",
        "🧪 Mô Phỏng Khí Hậu",
        "🗺️ Đối Chiếu Vùng Miền",
        "📅 Truy Vết Mùa Vụ",
        "🧠 Giải Mã Trọng Số & Thuật Toán"
    ])

    with tab1:
        render_alert_view(df, dt_model, rf_model)

    with tab2:
        render_climate_view(df, dt_model, rf_model)

    with tab3:
        render_regional_view(df)

    with tab4:
        render_seasonal_view(df)

    with tab5:
        render_explainability_view(df, dt_model, rf_model, evaluator)


if __name__ == "__main__":
    main()
