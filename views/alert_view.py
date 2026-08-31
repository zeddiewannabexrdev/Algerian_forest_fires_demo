import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import (
    WEATHER_FEATURES, FWI_FEATURES, ALL_MODEL_FEATURES, 
    FEATURE_NAMES_VI, FEATURE_RANGES, RISK_LEVELS
)


def get_risk_level_info(score: float) -> dict:
    for level in RISK_LEVELS:
        if level["min_score"] <= score <= level["max_score"]:
            return level
    return RISK_LEVELS[-1]


def create_gauge_chart(score: float, level_info: dict, palette: dict) -> go.Figure:
    paper_bg = palette["chart_paper"]
    text_color = palette["text_primary"]
    sub_color = palette["text_secondary"]
    border_color = palette["border"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score * 100,
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": f"<b>{level_info['badge']}</b><br><span style='font-size:13px; color:{sub_color}; font-weight:600'>{level_info['name']}</span>",
            "font": {"size": 18, "color": text_color, "family": "Segoe UI, Arial, sans-serif"}
        },
        number={"suffix": "%", "font": {"size": 38, "color": text_color, "family": "Consolas, monospace"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": sub_color, "tickfont": {"size": 11, "color": sub_color, "family": "Consolas, monospace"}},
            "bar": {"color": level_info["color"], "thickness": 0.26},
            "bgcolor": paper_bg,
            "borderwidth": 1,
            "bordercolor": border_color,
            "steps": [
                {"range": [0, 25], "color": "rgba(46, 111, 64, 0.25)"},
                {"range": [25, 50], "color": "rgba(154, 106, 18, 0.25)"},
                {"range": [50, 75], "color": "rgba(180, 67, 26, 0.25)"},
                {"range": [75, 100], "color": "rgba(153, 27, 27, 0.25)"}
            ],
            "threshold": {
                "line": {"color": text_color, "width": 2},
                "thickness": 0.6,
                "value": 75
            }
        }
    ))

    fig.update_layout(
        height=260,
        margin=dict(l=25, r=25, t=40, b=15),
        paper_bgcolor=paper_bg,
        font={"family": "Segoe UI, Arial, sans-serif"}
    )
    return fig


def render_alert_view(df: pd.DataFrame, dt_model, rf_model, palette: dict):
    text_pri = palette["text_primary"]
    text_sec = palette["text_secondary"]
    text_mut = palette["text_muted"]
    card_bg = palette["bg_card"]
    border_col = palette["border"]
    tag_bg = palette["tag_bg"]

    st.markdown(f"<h4 style='color:{text_pri}; margin:0;'>GIÁM SÁT RỦI RO & CẢNH BÁO TỨC THỜI</h4>", unsafe_allow_html=True)
    st.caption("Truyền thông số trắc lượng hiện trường để tính toán xác suất bắt lửa từ hai động cơ học máy độc lập.")

    # Historical record lookup option for quick verification
    col_preset, _ = st.columns([3, 1])
    with col_preset:
        use_sample = st.checkbox("Sử dụng dữ liệu mẫu từ nhật ký quan trắc lịch sử", value=False)
    
    sample_values = {}
    if use_sample:
        selected_idx = st.selectbox(
            "Bản ghi quan trắc:",
            options=df.index.tolist(),
            format_func=lambda i: f"Ngày {df.loc[i, 'Date'].strftime('%d/%m/%Y')} | {df.loc[i, 'Region']} | Thực tế: {df.loc[i, 'Classes'].upper()}"
        )
        sample_row = df.loc[selected_idx]
        for f in ALL_MODEL_FEATURES:
            sample_values[f] = float(sample_row[f])

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    # Input controls
    col_input1, col_input2 = st.columns(2)
    inputs = {}

    with col_input1:
        st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Quan Trắc Khí Tượng Thực Địa</div>", unsafe_allow_html=True)
        for feat in WEATHER_FEATURES:
            cfg = FEATURE_RANGES[feat]
            val = sample_values.get(feat, cfg["default"])
            inputs[feat] = st.slider(
                f"{FEATURE_NAMES_VI[feat]}",
                min_value=float(cfg["min"]),
                max_value=float(cfg["max"]),
                value=float(val),
                step=float(cfg["step"]),
                key=f"alert_input_{feat}"
            )

    with col_input2:
        st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Chỉ Số Vật Liệu Cháy (FWI System)</div>", unsafe_allow_html=True)
        for feat in FWI_FEATURES:
            cfg = FEATURE_RANGES[feat]
            val = sample_values.get(feat, cfg["default"])
            inputs[feat] = st.slider(
                f"{FEATURE_NAMES_VI[feat]}",
                min_value=float(cfg["min"]),
                max_value=float(cfg["max"]),
                value=float(val),
                step=float(cfg["step"]),
                key=f"alert_input_{feat}"
            )

    input_df = pd.DataFrame([inputs])[ALL_MODEL_FEATURES]

    # Model inference
    dt_prob = dt_model.predict_proba(input_df)[0][1]
    rf_prob = rf_model.predict_proba(input_df)[0][1]
    dt_pred = dt_model.predict(input_df)[0]
    rf_pred = rf_model.predict(input_df)[0]

    # Equal ensemble risk aggregation
    ensemble_prob = 0.5 * dt_prob + 0.5 * rf_prob
    level_info = get_risk_level_info(ensemble_prob)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Chỉ Số Rủi Ro Tổng Hợp & Đánh Giá Độc Lập</div>", unsafe_allow_html=True)

    col_gauge, col_models = st.columns([1.2, 1])

    with col_gauge:
        st.plotly_chart(create_gauge_chart(ensemble_prob, level_info, palette), use_container_width=True)

    with col_models:
        dt_text = "NGUY CƠ CHÁY" if dt_pred == 1 else "AN TOÀN"
        rf_text = "NGUY CƠ CHÁY" if rf_pred == 1 else "AN TOÀN"
        tree_agree = rf_model.get_tree_agreement(input_df)

        st.markdown(f"""
        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-left: 4px solid #475569; padding: 12px 14px; border-radius: 4px; margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 12px; font-weight: 700; color: {text_sec}; letter-spacing: 0.5px; text-transform: uppercase;">Decision Tree Engine</span>
                <span style="font-family: Consolas, monospace; font-size: 13px; font-weight: 700; color: {text_pri};">P = {dt_prob * 100:.1f}%</span>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: {text_pri}; margin-top: 4px;">{dt_text}</div>
        </div>

        <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-left: 4px solid {level_info['color']}; padding: 12px 14px; border-radius: 4px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 12px; font-weight: 700; color: {text_sec}; letter-spacing: 0.5px; text-transform: uppercase;">Random Forest Engine</span>
                <span style="font-family: Consolas, monospace; font-size: 13px; font-weight: 700; color: {text_pri};">P = {rf_prob * 100:.1f}%</span>
            </div>
            <div style="font-size: 16px; font-weight: 700; color: {text_pri}; margin-top: 4px;">{rf_text}</div>
            <div style="font-size: 12px; color: {text_sec}; margin-top: 4px; font-family: Consolas, monospace; font-weight: 600;">Độ đồng thuận: {tree_agree['fire_votes']}/{tree_agree['total_trees']} cây ({tree_agree['agreement_ratio']:.0f}%)</div>
        </div>
        """, unsafe_allow_html=True)

    # Operational directive
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="border: 1px solid {border_col}; border-top: 4px solid {level_info['color']}; border-radius: 4px; padding: 14px 18px; background-color: {card_bg};">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
            <span style="font-weight: 700; color: {text_pri}; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;">Chỉ Thị Tác Chiến: {level_info['name']}</span>
            <span style="font-size: 12px; font-weight: 700; background-color: {tag_bg}; color: {text_pri}; border: 1px solid {border_col}; padding: 3px 10px; border-radius: 3px; font-family: Consolas, monospace;">{level_info['badge']}</span>
        </div>
        <div style="font-size: 13px; color: {text_sec}; font-weight: 500; margin-bottom: 10px;">{level_info['description']}</div>
        <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: {text_sec}; line-height: 1.8;">
            {''.join([f"<li>{act}</li>" for act in level_info['actions']])}
        </ul>
    </div>
    """, unsafe_allow_html=True)
