import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import CLIMATE_PRESETS, ALL_MODEL_FEATURES


def render_climate_view(df: pd.DataFrame, dt_model, rf_model):
    st.markdown("### 🧪 Mô Phỏng Kịch Bản Khí Hậu & Phân Tích Độ Nhạy Rủi Ro (What-If Analysis)")
    st.caption("Giả lập tác động của các biến động khí hậu cực đoan đến khả năng bùng phát cháy rừng và so sánh cách 2 thuật toán phản ứng.")

    st.subheader("1. Chọn Kịch Bản Khí Hậu Mẫu")
    preset_key = st.radio(
        "Lựa chọn kịch bản giả lập:",
        options=list(CLIMATE_PRESETS.keys()),
        format_func=lambda k: f"{CLIMATE_PRESETS[k]['title']} — {CLIMATE_PRESETS[k]['desc']}",
        horizontal=False
    )
    preset = CLIMATE_PRESETS[preset_key]
    delta = preset["delta"]

    base_values = df[ALL_MODEL_FEATURES].median().to_dict()

    st.markdown("##### 🎛️ Tinh Chỉnh Biến Số Khí Hậu Giả Lập")
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
        st.metric(label="Xác suất cháy - Decision Tree", value=f"{prob_dt:.1f}%", delta=f"{prob_dt - 50:.1f}% so với ngưỡng cắt 50%")
    with col_res2:
        st.metric(label="Xác suất cháy - Random Forest", value=f"{prob_rf:.1f}%", delta=f"{prob_rf - 50:.1f}% so với ngưỡng cắt 50%")

    st.markdown("---")
    st.subheader("2. Đường Cong Phản Ứng Độ Nhạy (Temperature Sensitivity Curve)")
    st.caption("Khảo sát sự thay đổi xác suất rủi ro khi nhiệt độ tăng liên tục từ 20°C đến 45°C (giữ nguyên độ ẩm và các yếu tố khác).")

    temp_range = np.linspace(20, 45, 50)
    curve_dt = []
    curve_rf = []

    for t in temp_range:
        temp_sim = sim_row.copy()
        temp_sim["Temperature"] = t
        temp_sim["FFMC"] = np.clip(base_values["FFMC"] + (t - 30) * 1.5 - (sim_rh - 60) * 0.4, 30.0, 96.0)
        temp_sim["ISI"] = np.clip(base_values["ISI"] + (sim_ws - 15) * 0.3 + (t - 30) * 0.3, 0.0, 19.0)
        curve_dt.append(dt_model.predict_proba(temp_sim)[0][1] * 100)
        curve_rf.append(rf_model.predict_proba(temp_sim)[0][1] * 100)

    fig_curve = go.Figure()
    fig_curve.add_trace(go.Scatter(
        x=temp_range, y=curve_dt,
        mode="lines",
        name="Decision Tree (Phản ứng dạng bậc thang / Ngưỡng cứng)",
        line=dict(color="#3b82f6", width=2.5, dash="dash")
    ))
    fig_curve.add_trace(go.Scatter(
        x=temp_range, y=curve_rf,
        mode="lines",
        name="Random Forest (Phản ứng mượt mà / Sigmoid mờ)",
        line=dict(color="#ef4444", width=3.5)
    ))
    fig_curve.add_hline(y=50, line_dash="dot", line_color="gray", annotation_text="Ngưỡng kích hoạt Cháy (50%)")
    fig_curve.add_vline(x=sim_temp, line_dash="longdash", line_color="#10b981", annotation_text=f"Nhiệt độ hiện tại ({sim_temp}°C)")

    fig_curve.update_layout(
        xaxis_title="Nhiệt độ (°C)",
        yaxis_title="Xác suất bùng phát Cháy (%)",
        height=380,
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.02)
    )
    st.plotly_chart(fig_curve, use_container_width=True)

    st.markdown("---")
    st.subheader("3. Ma Trận Ranh Giới Chuyển Pha Bắt Lửa 2D (Tipping Point Heatmap)")
    st.caption("Bản đồ ranh giới rủi ro tương tác giữa Nhiệt độ (°C) và Độ ẩm không khí (%):")

    grid_t = np.linspace(22, 42, 20)
    grid_rh = np.linspace(25, 90, 20)
    T_grid, RH_grid = np.meshgrid(grid_t, grid_rh)

    Z_dt = np.zeros(T_grid.shape)
    Z_rf = np.zeros(T_grid.shape)

    for i in range(T_grid.shape[0]):
        for j in range(T_grid.shape[1]):
            t_val = T_grid[i, j]
            rh_val = RH_grid[i, j]
            sample = sim_row.copy()
            sample["Temperature"] = t_val
            sample["RH"] = rh_val
            sample["FFMC"] = np.clip(base_values["FFMC"] + (t_val - 30) * 1.5 - (rh_val - 60) * 0.4, 30.0, 96.0)
            sample["ISI"] = np.clip(base_values["ISI"] + (sim_ws - 15) * 0.3 + (t_val - 30) * 0.3, 0.0, 19.0)
            Z_dt[i, j] = dt_model.predict_proba(sample)[0][1] * 100
            Z_rf[i, j] = rf_model.predict_proba(sample)[0][1] * 100

    fig_contour = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Decision Tree (Phân định ranh giới trực giao cứng)", "Random Forest (Biên độ chuyển tiếp liên tục)")
    )

    fig_contour.add_trace(
        go.Contour(
            z=Z_dt, x=grid_t, y=grid_rh,
            colorscale="YlOrRd",
            contours=dict(coloring="heatmap", showlabels=True),
            colorbar=dict(title="Rủi ro (%)", len=0.8),
            showscale=False
        ),
        row=1, col=1
    )

    fig_contour.add_trace(
        go.Contour(
            z=Z_rf, x=grid_t, y=grid_rh,
            colorscale="YlOrRd",
            contours=dict(coloring="heatmap", showlabels=True),
            colorbar=dict(title="Rủi ro (%)", len=0.8),
            showscale=True
        ),
        row=1, col=2
    )

    fig_contour.update_xaxes(title_text="Nhiệt độ (°C)", row=1, col=1)
    fig_contour.update_xaxes(title_text="Nhiệt độ (°C)", row=1, col=2)
    fig_contour.update_yaxes(title_text="Độ ẩm tương đối (%)", row=1, col=1)
    fig_contour.update_yaxes(title_text="Độ ẩm tương đối (%)", row=1, col=2)

    fig_contour.update_layout(height=450, margin=dict(l=40, r=40, t=50, b=40))
    st.plotly_chart(fig_contour, use_container_width=True)

    st.info("💡 **Ghi chú phân tích thuật toán**: Decision Tree tạo ra các phân vùng vuông góc (axis-aligned orthogonal splits) dẫn đến hiện tượng 'nhảy bước' khi một thông số vượt qua ngưỡng rẽ nhánh. Ngược lại, Random Forest tổng hợp từ 100 cây con nên tạo ra bề mặt ranh giới mềm mại, phản ánh sát hơn tính chất vật lý của tự nhiên.")
