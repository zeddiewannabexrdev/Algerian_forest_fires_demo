import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from config import (
    WEATHER_FEATURES, FWI_FEATURES, ALL_MODEL_FEATURES, 
    FEATURE_NAMES_VI, FEATURE_RANGES, RISK_LEVELS
)


def get_risk_level_info(score: float) -> dict:
    for level in RISK_LEVELS:
        if level["min_score"] <= score <= level["max_score"]:
            return level
    return RISK_LEVELS[-1]


def create_gauge_chart(score: float, level_info: dict) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score * 100,
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": f"<b>{level_info['badge']}</b><br><span style='font-size:13px; color:gray'>{level_info['name']}</span>", "font": {"size": 20}},
        number={"suffix": "%", "font": {"size": 38, "color": level_info["color"], "family": "Arial"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "gray"},
            "bar": {"color": level_info["color"], "thickness": 0.28},
            "bgcolor": "white",
            "borderwidth": 1,
            "bordercolor": "#e5e7eb",
            "steps": [
                {"range": [0, 25], "color": "rgba(16, 185, 129, 0.2)"},
                {"range": [25, 50], "color": "rgba(245, 158, 11, 0.2)"},
                {"range": [50, 75], "color": "rgba(249, 115, 22, 0.25)"},
                {"range": [75, 100], "color": "rgba(239, 68, 68, 0.3)"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 75
            }
        }
    ))

    fig.update_layout(
        height=280,
        margin=dict(l=25, r=25, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "sans-serif"}
    )
    return fig


def render_alert_view(df: pd.DataFrame, dt_model, rf_model):
    st.markdown("### 🚨 Hệ Thống Cảnh Báo Sớm & Đánh Giá Rủi Ro Cháy Rừng")
    st.caption("Nhập dữ liệu trắc lượng khí hậu & các chỉ số vật liệu cháy FWI để nhận cảnh báo tức thời từ 2 thuật toán độc lập.")

    # Historical record lookup option for quick verification
    col_preset, _ = st.columns([3, 1])
    with col_preset:
        use_sample = st.checkbox("🔍 Dùng thử 1 bản ghi thực tế từ cơ sở dữ liệu để kiểm nghiệm", value=False)
    
    sample_values = {}
    if use_sample:
        selected_idx = st.selectbox(
            "Chọn ngày kiểm tra:",
            options=df.index.tolist(),
            format_func=lambda i: f"Ngày {df.loc[i, 'Date'].strftime('%d/%m/%Y')} - {df.loc[i, 'Region']} (Thực tế: {df.loc[i, 'Classes'].upper()})"
        )
        sample_row = df.loc[selected_idx]
        for f in ALL_MODEL_FEATURES:
            sample_values[f] = float(sample_row[f])

    st.markdown("---")
    st.subheader("1. Tham Số Khí Tượng & Chỉ Số Vật Liệu Cháy (FWI)")

    col_input1, col_input2 = st.columns(2)
    inputs = {}

    with col_input1:
        st.markdown("##### 🌤️ Yếu Tố Thời Tiết Thực Địa")
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
        st.markdown("##### 🔥 Chỉ Số Hệ Thống FWI (Canadian System)")
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

    st.markdown("---")
    st.subheader("2. Kết Quả Giám Định & Cấp Độ Cảnh Báo Tức Thời")

    col_gauge, col_models = st.columns([1.2, 1])

    with col_gauge:
        st.plotly_chart(create_gauge_chart(ensemble_prob, level_info), use_container_width=True)

    with col_models:
        st.markdown("##### 🤖 Kết Quả Từng Thuật Toán")
        
        dt_badge_color = "#ef4444" if dt_pred == 1 else "#10b981"
        dt_text = "NGUY CƠ CHÁY" if dt_pred == 1 else "AN TOÀN"
        st.markdown(f"""
        <div style="background-color: #f8fafc; border-left: 5px solid {dt_badge_color}; padding: 10px 14px; border-radius: 6px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-weight: 600; font-size: 14px; color: #334155;">🌳 Cây Quyết Định (Decision Tree)</div>
            <div style="font-size: 18px; font-weight: bold; color: {dt_badge_color}; margin: 3px 0;">{dt_text}</div>
            <div style="font-size: 12px; color: #64748b;">Xác suất cháy: <b>{dt_prob * 100:.1f}%</b></div>
        </div>
        """, unsafe_allow_html=True)

        rf_badge_color = "#ef4444" if rf_pred == 1 else "#10b981"
        rf_text = "NGUY CƠ CHÁY" if rf_pred == 1 else "AN TOÀN"
        tree_agree = rf_model.get_tree_agreement(input_df)
        st.markdown(f"""
        <div style="background-color: #f8fafc; border-left: 5px solid {rf_badge_color}; padding: 10px 14px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="font-weight: 600; font-size: 14px; color: #334155;">🌲 Rừng Ngẫu Nhiên (Random Forest)</div>
            <div style="font-size: 18px; font-weight: bold; color: {rf_badge_color}; margin: 3px 0;">{rf_text}</div>
            <div style="font-size: 12px; color: #64748b;">Xác suất cháy: <b>{rf_prob * 100:.1f}%</b> | Đồng thuận: <b>{tree_agree['fire_votes']}/{tree_agree['total_trees']} cây</b></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("3. 📋 Phương Án Tác Chiến Khuyến Nghị Cho Lực Lượng Lâm Nghiệp")

    st.markdown(f"""
    <div style="border: 2px solid {level_info['color']}; border-radius: 8px; padding: 15px 20px; background-color: {level_info['color']}10;">
        <h4 style="color: {level_info['color']}; margin-top: 0;">{level_info['name']} - Tình trạng: {level_info['description']}</h4>
        <ul style="margin-bottom: 0; padding-left: 20px; line-height: 1.8;">
            {''.join([f"<li><b>{act}</b></li>" for act in level_info['actions']])}
        </ul>
    </div>
    """, unsafe_allow_html=True)
