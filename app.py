import importlib
import streamlit as st
import pandas as pd

import config
if not hasattr(config, "get_theme_palette"):
    importlib.reload(config)
from config import get_theme_palette
from data_loader import load_and_clean_data, get_feature_data
from models import ModelEvaluator
from views import (
    render_alert_view,
    render_climate_view,
    render_regional_view,
    render_seasonal_view,
    render_explainability_view
)

st.set_page_config(
    page_title="Hệ Thống Phân Tích & Cảnh Báo Cháy Rừng",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource(show_spinner=False)
def init_models_and_evaluator(df: pd.DataFrame):
    X, y = get_feature_data(df)
    evaluator = ModelEvaluator(test_size=0.2, random_state=42)
    evaluator.fit_and_evaluate(X, y)
    return evaluator


def main():
    df = load_and_clean_data()
    evaluator = init_models_and_evaluator(df)
    dt_model = evaluator.dt_manager
    rf_model = evaluator.rf_manager

    # Sidebar: Clean functional control panel
    with st.sidebar:
        st.markdown("<div style='font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;'>BẢNG ĐIỀU KHIỂN HỆ THỐNG</div>", unsafe_allow_html=True)
        st.caption("Forest Fire Analytics Workstation v2.0")
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)

        # Theme Switcher
        theme_mode = st.radio(
            "Chế độ hiển thị (Theme):",
            options=["Tối (Dark Mode)", "Sáng (Light Mode)"],
            index=0,
            horizontal=True
        )
        is_dark = "Tối" in theme_mode
        palette = get_theme_palette(is_dark)

        st.markdown(f"<div style='border-bottom: 1px solid {palette['border']}; margin: 12px 0;'></div>", unsafe_allow_html=True)

        st.markdown(f"<div style='font-size: 11px; font-weight: 700; color: {palette['text_secondary']}; text-transform: uppercase; margin-bottom: 6px;'>Thông Số Dữ Liệu</div>", unsafe_allow_html=True)
        total_samples = len(df)
        fire_samples = int(df["Fire_Label"].sum())
        safe_samples = total_samples - fire_samples

        fire_text_col = "#ef4444" if is_dark else "#991b1b"
        safe_text_col = "#38bdf8" if is_dark else "#2e6f40"

        st.markdown(f"""
        <div style="background: {palette['bg_surface']}; border: 1px solid {palette['border']}; border-radius: 4px; padding: 12px 14px; font-size: 12px; line-height: 1.8; color: {palette['text_secondary']}; margin-bottom: 14px;">
            <div>Tổng quan trắc: <b style="font-family: Consolas, monospace; color: {palette['text_primary']};">{total_samples}</b> ngày</div>
            <div>Bản ghi cháy: <b style="font-family: Consolas, monospace; color: {fire_text_col};">{fire_samples}</b> ({fire_samples/total_samples*100:.1f}%)</div>
            <div>Bản ghi an toàn: <b style="font-family: Consolas, monospace; color: {safe_text_col};">{safe_samples}</b> ({safe_samples/total_samples*100:.1f}%)</div>
            <div>Vùng Bejaia: <b style="font-family: Consolas, monospace; color: {palette['text_primary']};">122</b> mẫu (Duyên hải)</div>
            <div>Vùng Sidi-Bel Abbes: <b style="font-family: Consolas, monospace; color: {palette['text_primary']};">122</b> mẫu (Nội địa)</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<div style='font-size: 11px; font-weight: 700; color: {palette['text_secondary']}; text-transform: uppercase; margin-bottom: 6px;'>Trạng Thái Động Cơ Học Máy</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: {palette['bg_surface']}; border: 1px solid {palette['border']}; border-radius: 4px; padding: 12px 14px; font-size: 12px; line-height: 1.8; color: {palette['text_secondary']}; margin-bottom: 14px;">
            <div>Decision Tree Acc: <b style="font-family: Consolas, monospace; color: {palette['text_primary']};">{evaluator.dt_eval['accuracy']*100:.1f}%</b></div>
            <div>Random Forest Acc: <b style="font-family: Consolas, monospace; color: {palette['text_primary']};">{evaluator.rf_eval['accuracy']*100:.1f}%</b></div>
            <div>Phân bổ kiểm thử: <b style="font-family: Consolas, monospace; color: {palette['text_primary']};">20% Stratified</b></div>
            <div>Trạng thái: <span style="font-family: Consolas, monospace; color: {safe_text_col}; font-weight: 700;">HOẠT ĐỘNG</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"<div style='font-size: 11px; font-weight: 700; color: {palette['text_secondary']}; text-transform: uppercase; margin-bottom: 6px;'>Tệp Nguồn Hoạt Động</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-family: Consolas, monospace; font-size: 11px; font-weight: 600; color: {palette['text_primary']}; background: {palette['bg_surface']}; padding: 8px 10px; border-radius: 4px; border: 1px solid {palette['border']}; word-break: break-all;">
            data/Algerian_forest_fires_dataset_UPDATE.csv
        </div>
        """, unsafe_allow_html=True)

    # Dynamic Theme CSS Injection
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: {palette['bg_app']} !important;
            color: {palette['text_primary']} !important;
        }}
        
        section[data-testid="stSidebar"] {{
            background-color: {palette['bg_card']} !important;
            border-right: 1px solid {palette['border']} !important;
        }}

        section[data-testid="stSidebar"] div,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {{
            color: {palette['text_primary']} !important;
        }}

        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 96%;
        }}

        /* Clean Software Header */
        .app-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid {palette['border']};
            padding-bottom: 12px;
            margin-bottom: 16px;
            background-color: transparent;
        }}
        .app-title {{
            font-size: 18px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: {palette['text_primary']};
            text-transform: uppercase;
            margin: 0;
        }}
        .app-subtitle {{
            font-size: 13px;
            color: {palette['text_secondary']};
            font-weight: 500;
            margin: 3px 0 0 0;
        }}
        .app-telemetry {{
            font-family: Consolas, "SF Mono", Monaco, monospace;
            font-size: 11px;
            font-weight: 600;
            color: {palette['text_primary']};
            background-color: {palette['bg_surface']};
            border: 1px solid {palette['border']};
            padding: 5px 12px;
            border-radius: 3px;
        }}

        /* Workstation Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 4px;
            border-bottom: 1px solid {palette['border']};
            background-color: transparent;
        }}
        .stTabs [data-baseweb="tab"] {{
            padding: 9px 18px;
            border-radius: 4px 4px 0 0;
            font-size: 13px;
            font-weight: 600;
            color: {palette['text_secondary']};
            background-color: {palette['bg_surface']};
            border: 1px solid {palette['border']};
            border-bottom: none;
        }}
        .stTabs [aria-selected="true"] {{
            color: {palette['text_primary']} !important;
            font-weight: 700 !important;
            background-color: {palette['bg_card']} !important;
            border-color: {palette['border_accent']} !important;
            border-bottom: 2px solid {palette['accent_line']} !important;
        }}

        /* Form Labels & Inputs */
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] span,
        div[data-testid="stMarkdownContainer"] li {{
            color: {palette['text_secondary']};
        }}

        label, .stSlider label, .stSelectbox label, .stRadio label {{
            color: {palette['text_primary']} !important;
            font-weight: 600 !important;
        }}

        footer {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

    # Main Application Shell Header
    st.markdown(f"""
    <div class="app-header">
        <div>
            <h1 class="app-title">Hệ Thống Phân Tích & Dự Báo Nguy Cơ Cháy Rừng</h1>
            <p class="app-subtitle">Trung tâm điều hành hỗ trợ ra quyết định lâm nghiệp tích hợp học máy</p>
        </div>
        <div class="app-telemetry">
            HỆ THỐNG: SẴN SÀNG | 244 BẢN GHI | DUAL-ENGINE: DT / RF
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Workstation Navigation Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "GIÁM SÁT TỨC THỜI",
        "MÔ PHỎNG KHÍ HẬU",
        "ĐỐI CHIẾU VÙNG",
        "TIẾN TRÌNH MÙA VỤ",
        "GIẢI MÃ THUẬT TOÁN"
    ])

    with tab1:
        render_alert_view(df, dt_model, rf_model, palette)

    with tab2:
        render_climate_view(df, dt_model, rf_model, palette)

    with tab3:
        render_regional_view(df, palette)

    with tab4:
        render_seasonal_view(df, palette)

    with tab5:
        render_explainability_view(df, dt_model, rf_model, evaluator, palette)


if __name__ == "__main__":
    main()
