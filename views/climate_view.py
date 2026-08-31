import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import CLIMATE_PRESETS, ALL_MODEL_FEATURES


def render_climate_view(df: pd.DataFrame, dt_model, rf_model, palette: dict):
    text_pri = palette["text_primary"]
    text_sec = palette["text_secondary"]
    border_col = palette["border"]
    card_bg = palette["bg_card"]
    paper_bg = palette["chart_paper"]
    plot_bg = palette["chart_plot"]
    grid_col = palette["chart_grid"]
    is_dark = palette["is_dark"]
    font_title = palette.get("font_title", "Montserrat, sans-serif")
    font_body = palette.get("font_body", "Lato, sans-serif")

    st.markdown(f"<h4 style='color:{text_pri}; margin:0; font-family:{font_title};'>MÔ PHỎNG KỊCH BẢN KHÍ HẬU & ĐỘ NHẠY RỦI RO</h4>", unsafe_allow_html=True)
    st.caption("Khảo nghiệm phản ứng của mô hình trước các biến thiên khí hậu cực đoan và định vị ranh giới chuyển pha bắt lửa.")

    st.markdown(f"<div style='font-family: {font_title}; font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Kịch Bản Giả Lập Mẫu</div>", unsafe_allow_html=True)
    preset_key = st.radio(
        "Kịch bản:",
        options=list(CLIMATE_PRESETS.keys()),
        format_func=lambda k: f"{CLIMATE_PRESETS[k]['title']} — {CLIMATE_PRESETS[k]['desc']}",
        horizontal=False,
        label_visibility="collapsed"
    )
    preset = CLIMATE_PRESETS[preset_key]
    delta = preset["delta"]

    base_values = df[ALL_MODEL_FEATURES].median().to_dict()

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Điều Chỉnh Tham Số Biến Đổi</div>", unsafe_allow_html=True)
    col_t, col_rh, col_ws, col_rain = st.columns(4)

    with col_t:
        sim_temp = st.slider(
            "Nhiệt độ (°C)",
            min_value=20.0, max_value=48.0,
            value=float(np.clip(base_values["Temperature"] + delta.get("Temperature", 0), 20.0, 48.0)),
            step=0.5
        )
    with col_rh:
        sim_rh = st.slider(
            "Độ ẩm tương đối (%)",
            min_value=15.0, max_value=95.0,
            value=float(np.clip(base_values["RH"] + delta.get("RH", 0), 15.0, 95.0)),
            step=1.0
        )
    with col_ws:
        sim_ws = st.slider(
            "Tốc độ gió (km/h)",
            min_value=5.0, max_value=32.0,
            value=float(np.clip(base_values["Ws"] + delta.get("Ws", 0), 5.0, 32.0)),
            step=1.0
        )
    with col_rain:
        sim_rain = st.slider(
            "Lượng mưa (mm)",
            min_value=0.0, max_value=20.0,
            value=float(np.clip(base_values["Rain"] + delta.get("Rain", 0), 0.0, 20.0)),
            step=0.2
        )

    # Dynamic FWI approximation under simulated climate shifts
    sim_ffmc = np.clip(base_values["FFMC"] + (sim_temp - 30) * 1.5 - (sim_rh - 60) * 0.4 - sim_rain * 5, 30.0, 96.0)
    sim_isi = np.clip(base_values["ISI"] + (sim_ws - 15) * 0.3 + (sim_temp - 30) * 0.3 - sim_rain * 1.5, 0.0, 19.0)
    sim_dmc = np.clip(base_values["DMC"] + (sim_temp - 30) * 0.8 - sim_rain * 2, 1.0, 65.0)
    sim_dc = np.clip(base_values["DC"] + (sim_temp - 30) * 1.5, 10.0, 220.0)
    sim_bui = np.clip(base_values["BUI"] + (sim_temp - 30) * 0.5, 2.0, 65.0)
    sim_fwi = np.clip(base_values["FWI"] + (sim_isi * 0.6) + (sim_bui * 0.3), 0.0, 32.0)

    sim_row = pd.DataFrame([{
        "Temperature": sim_temp,
        "RH": sim_rh,
        "Ws": sim_ws,
        "Rain": sim_rain,
        "FFMC": sim_ffmc,
        "DMC": sim_dmc,
        "DC": sim_dc,
        "ISI": sim_isi,
        "BUI": sim_bui,
        "FWI": sim_fwi
    }])[ALL_MODEL_FEATURES]

    prob_dt = dt_model.predict_proba(sim_row)[0][1] * 100
    prob_rf = rf_model.predict_proba(sim_row)[0][1] * 100

    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.markdown(f"""
        <div style="border: 1px solid {border_col}; border-radius: 4px; padding: 12px 16px; background: {card_bg};">
            <div style="font-family: {palette['font_title']}; font-size: 12px; font-weight: 700; color: {text_sec}; text-transform: uppercase;">Xác suất cháy (Decision Tree)</div>
            <div style="font-size: 24px; font-family: Consolas, monospace; font-weight: 700; color: {text_pri}; margin-top: 2px;">{prob_dt:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    with col_res2:
        st.markdown(f"""
        <div style="border: 1px solid {border_col}; border-radius: 4px; padding: 12px 16px; background: {card_bg};">
            <div style="font-family: {palette['font_title']}; font-size: 12px; font-weight: 700; color: {text_sec}; text-transform: uppercase;">Xác suất cháy (Random Forest)</div>
            <div style="font-size: 24px; font-family: Consolas, monospace; font-weight: 700; color: {text_pri}; margin-top: 2px;">{prob_rf:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family: {font_title}; font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Đường Cong Phản Ứng Độ Nhạy Nhiệt Độ (20°C Đến 45°C)</div>", unsafe_allow_html=True)

    temp_range = np.linspace(20, 45, 40)
    curve_samples = []
    for t in temp_range:
        s = sim_row.iloc[0].to_dict()
        s["Temperature"] = t
        s["FFMC"] = np.clip(base_values["FFMC"] + (t - 30) * 1.5 - (sim_rh - 60) * 0.4, 30.0, 96.0)
        s["ISI"] = np.clip(base_values["ISI"] + (sim_ws - 15) * 0.3 + (t - 30) * 0.3, 0.0, 19.0)
        curve_samples.append(s)

    curve_df = pd.DataFrame(curve_samples)[ALL_MODEL_FEATURES]
    curve_dt = dt_model.predict_proba(curve_df)[:, 1] * 100
    curve_rf = rf_model.predict_proba(curve_df)[:, 1] * 100

    rf_line_color = "#38bdf8" if is_dark else "#090d16"
    dt_line_color = "#94a3b8" if is_dark else "#475569"
    vline_color = "#38bdf8" if is_dark else "#090d16"

    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(
        x=temp_range, y=curve_dt,
        mode="lines",
        name="Decision Tree (Trực giao)",
        line=dict(color=dt_line_color, width=2, dash="dash")
    ))
    fig_curve.add_trace(go.Scatter(
        x=temp_range, y=curve_rf,
        mode="lines",
        name="Random Forest (Mượt mà)",
        line=dict(color=rf_line_color, width=2.5)
    ))
    fig_curve.add_hline(y=50, line_dash="dot", line_color=grid_col, annotation_text="Ngưỡng 50%", annotation_font_size=11, annotation_font_color=text_sec)
    fig_curve.add_vline(x=sim_temp, line_dash="solid", line_color=vline_color, line_width=1, annotation_text=f"{sim_temp}°C", annotation_font_size=11, annotation_font_color=text_pri)

    fig_curve.update_layout(
        xaxis=dict(title=dict(text="Nhiệt độ (°C)", font=dict(color=text_pri, size=12, family=font_title)), gridcolor=grid_col, zeroline=False, tickfont=dict(color=text_sec, family=font_body)),
        yaxis=dict(title=dict(text="Xác suất cháy (%)", font=dict(color=text_pri, size=12, family=font_title)), gridcolor=grid_col, zeroline=False, tickfont=dict(color=text_sec, family=font_body)),
        height=320,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": font_body, "color": text_pri, "size": 12},
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.96, xanchor="left", x=0.03, bgcolor=card_bg, bordercolor=border_col, borderwidth=1, font=dict(color=text_pri, family=font_body)),
        margin=dict(l=30, r=30, t=20, b=30)
    )
    st.plotly_chart(fig_curve, use_container_width=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family: {font_title}; font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Ma Trận Ranh Giới Chuyển Pha Bắt Lửa (Nhiệt Độ x Độ Ẩm)</div>", unsafe_allow_html=True)

    # Vectorized fast 2D grid generation
    grid_t = np.linspace(22, 42, 20)
    grid_rh = np.linspace(25, 90, 20)
    T_grid, RH_grid = np.meshgrid(grid_t, grid_rh)

    batch_samples = []
    for i in range(T_grid.shape[0]):
        for j in range(T_grid.shape[1]):
            t_val = T_grid[i, j]
            rh_val = RH_grid[i, j]
            batch_samples.append({
                "Temperature": t_val,
                "RH": rh_val,
                "Ws": sim_ws,
                "Rain": sim_rain,
                "FFMC": np.clip(base_values["FFMC"] + (t_val - 30) * 1.5 - (rh_val - 60) * 0.4, 30.0, 96.0),
                "DMC": sim_dmc,
                "DC": sim_dc,
                "ISI": np.clip(base_values["ISI"] + (sim_ws - 15) * 0.3 + (t_val - 30) * 0.3, 0.0, 19.0),
                "BUI": sim_bui,
                "FWI": sim_fwi
            })

    batch_df = pd.DataFrame(batch_samples)[ALL_MODEL_FEATURES]
    Z_dt = dt_model.predict_proba(batch_df)[:, 1].reshape(T_grid.shape) * 100
    Z_rf = rf_model.predict_proba(batch_df)[:, 1].reshape(T_grid.shape) * 100

    if is_dark:
        contour_scale = [
            [0.0, "#131b2e"],
            [0.25, "#1e293b"],
            [0.50, "#334155"],
            [0.75, "#b4431a"],
            [1.00, "#ef4444"]
        ]
    else:
        contour_scale = [
            [0.0, "#f8fafc"],
            [0.25, "#e2e8f0"],
            [0.50, "#cbd5e1"],
            [0.75, "#b4431a"],
            [1.00, "#991b1b"]
        ]

    fig_contour = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Decision Tree (Phân định vuông góc)", "Random Forest (Biên độ chuyển tiếp mềm)")
    )

    fig_contour.add_trace(
        go.Contour(
            z=Z_dt, x=grid_t, y=grid_rh,
            colorscale=contour_scale,
            contours=dict(coloring="heatmap", showlabels=True, labelfont=dict(size=10, color=text_pri, family="Consolas, monospace")),
            showscale=False
        ),
        row=1, col=1
    )

    fig_contour.add_trace(
        go.Contour(
            z=Z_rf, x=grid_t, y=grid_rh,
            colorscale=contour_scale,
            contours=dict(coloring="heatmap", showlabels=True, labelfont=dict(size=10, color=text_pri, family="Consolas, monospace")),
            colorbar=dict(title=dict(text="Rủi ro (%)", font=dict(size=11, color=text_pri)), len=0.85, thickness=12, tickfont=dict(color=text_sec)),
            showscale=True
        ),
        row=1, col=2
    )

    fig_contour.update_xaxes(title_text="Nhiệt độ (°C)", row=1, col=1, gridcolor=grid_col, title_font=dict(color=text_pri, family=palette.get("font_title", "Montserrat, sans-serif")), tickfont=dict(color=text_sec, family=palette.get("font_body", "Lato, sans-serif")))
    fig_contour.update_xaxes(title_text="Nhiệt độ (°C)", row=1, col=2, gridcolor=grid_col, title_font=dict(color=text_pri, family=palette.get("font_title", "Montserrat, sans-serif")), tickfont=dict(color=text_sec, family=palette.get("font_body", "Lato, sans-serif")))
    fig_contour.update_yaxes(title_text="Độ ẩm (%)", row=1, col=1, gridcolor=grid_col, title_font=dict(color=text_pri, family=palette.get("font_title", "Montserrat, sans-serif")), tickfont=dict(color=text_sec, family=palette.get("font_body", "Lato, sans-serif")))
    fig_contour.update_yaxes(title_text="Độ ẩm (%)", row=1, col=2, gridcolor=grid_col, title_font=dict(color=text_pri, family=palette.get("font_title", "Montserrat, sans-serif")), tickfont=dict(color=text_sec, family=palette.get("font_body", "Lato, sans-serif")))

    fig_contour.update_layout(
        height=380,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": palette.get("font_body", "Lato, sans-serif"), "color": text_pri, "size": 12},
        margin=dict(l=30, r=30, t=40, b=30)
    )
    st.plotly_chart(fig_contour, use_container_width=True)

    st.markdown(f"""
    <div style="border-left: 3px solid {border_col}; padding-left: 12px; font-size: 13px; color: {text_sec}; font-weight: 500; margin-top: 6px; font-family: {palette['font_body']};">
        ĐẶC TÍNH MÔ HÌNH: Decision Tree áp dụng các lát cắt trực giao (axis-aligned orthogonal partitions), dẫn đến bước nhảy tức thời tại các điểm chia nhánh. Random Forest tổng hợp từ nhiều cây con với các tập thuộc tính con khác nhau, tạo bề mặt xác suất mượt mà và phân định ranh giới gần với quy luật tự nhiên.
    </div>
    """, unsafe_allow_html=True)
