import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import FEATURE_NAMES_VI


def render_seasonal_view(df: pd.DataFrame):
    st.markdown("### 📅 Truy Vết Rủi Ro Theo Mùa Vụ & Diễn Biến Thời Gian")
    st.caption("Giám sát chuỗi thời gian 4 tháng mùa hè (Tháng 6 - Tháng 9/2012), phát hiện quy luật tích lũy khô hạn và các điểm bùng phát cháy rừng đỉnh điểm.")

    col_region, _ = st.columns([2, 2])
    with col_region:
        sel_region = st.selectbox(
            "Phạm vi phân tích mùa vụ:",
            options=["Toàn bộ Algeria (Cả 2 vùng)", "Bejaia (Ven biển)", "Sidi-Bel Abbes (Nội địa)"]
        )

    if "Bejaia" in sel_region:
        df_view = df[df["Region"] == "Bejaia"].copy()
    elif "Sidi" in sel_region:
        df_view = df[df["Region"] == "Sidi-Bel Abbes"].copy()
    else:
        # Aggregate daily mean across both regions
        df_view = df.groupby("Date").agg({
            "day": "first",
            "month": "first",
            "Temperature": "mean",
            "RH": "mean",
            "Ws": "mean",
            "Rain": "mean",
            "FFMC": "mean",
            "DMC": "mean",
            "DC": "mean",
            "ISI": "mean",
            "BUI": "mean",
            "FWI": "mean",
            "Fire_Label": "max"
        }).reset_index()

    st.markdown("---")
    st.subheader("1. Chuỗi Thời Gian Diễn Biến Khí Hậu & Các Đợt Phát Hỏa")
    st.caption("Quan sát sự kết hợp giữa đỉnh nhiệt độ, sự suy giảm lượng mưa và các ngày bùng phát đám cháy:")

    fig_time = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Diễn biến Nhiệt độ (°C) & Lượng mưa (mm)", "Chỉ số nguy cơ FWI & Các ngày xảy ra Cháy")
    )

    fig_time.add_trace(
        go.Scatter(
            x=df_view["Date"], y=df_view["Temperature"],
            mode="lines+markers",
            name="Nhiệt độ (°C)",
            line=dict(color="#f97316", width=2)
        ),
        row=1, col=1
    )
    fig_time.add_trace(
        go.Bar(
            x=df_view["Date"], y=df_view["Rain"],
            name="Lượng mưa (mm)",
            marker_color="#0ea5e9",
            opacity=0.6
        ),
        row=1, col=1
    )

    fig_time.add_trace(
        go.Scatter(
            x=df_view["Date"], y=df_view["FWI"],
            mode="lines",
            name="Chỉ số FWI",
            line=dict(color="#8b5cf6", width=2)
        ),
        row=2, col=1
    )

    fire_days = df_view[df_view["Fire_Label"] == 1]
    fig_time.add_trace(
        go.Scatter(
            x=fire_days["Date"], y=fire_days["FWI"],
            mode="markers",
            name="Ngày Có Cháy",
            marker=dict(color="#ef4444", size=9, symbol="cross", line=dict(width=1, color="darkred"))
        ),
        row=2, col=1
    )

    fig_time.update_layout(
        height=520,
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_time, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Hiện Tượng Tích Lũy Khô Hạn Tầng Sâu (Drought Code - DC)")
    st.caption("Tại sao Tháng 8 lại là 'tháng cháy tồi tệ nhất' dù nhiệt độ có thể không chênh lệch nhiều so với Tháng 7?")

    col_dc1, col_dc2 = st.columns([1.6, 1])

    with col_dc1:
        fig_dc = px.line(
            df_view,
            x="Date",
            y=["DC", "DMC", "BUI"],
            labels={"value": "Điểm chỉ số", "variable": "Chỉ số độ ẩm mùn", "Date": "Ngày"},
            title="Đà tăng liên tục không ngừng của chỉ số khô hạn tầng sâu (DC) từ Tháng 6 đến Tháng 8",
            color_discrete_map={"DC": "#b91c1c", "DMC": "#f59e0b", "BUI": "#6366f1"}
        )
        fig_dc.update_layout(height=360, margin=dict(l=30, r=30, t=50, b=30))
        st.plotly_chart(fig_dc, use_container_width=True)

    with col_dc2:
        st.markdown("""
        <div style="background-color: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 15px; margin-top: 10px;">
            <h5 style="color: #991b1b; margin-top: 0;">🔥 Giải Mã Đỉnh Điểm Tháng 8</h5>
            <p style="font-size: 13px; color: #4b5563; line-height: 1.6;">
                - <b>Chỉ số DC (Drought Code)</b> đại diện cho hàm lượng ẩm của tầng hữu cơ sâu và thân cây gỗ mục lớn.<br>
                - Khác với tầng mặt (FFMC) có thể khô hoặc ẩm lại chỉ sau vài giờ, tầng sâu cần hàng chục ngày nắng liên tục để bốc hơi hết nước.<br>
                - Sang <b>Tháng 8</b>, chỉ số DC chạm ngưỡng kỷ lục <b>>150-200</b>. Khi đó, nếu xảy ra cháy, ngọn lửa sẽ cháy âm ỉ rất sâu dưới rễ cây, tỏa nhiệt lượng cực lớn và lan truyền không thể dập tắt bằng nước bề mặt.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("3. Ma Trận Lịch Rủi Ro Từng Ngày Theo Tháng (Calendar Heatmap)")
    st.caption("Bản đồ nhiệt ma trận: Trục hoành là ngày trong tháng (1 đến 31), trục tung là Tháng quan trắc:")

    # Monthly calendar risk matrix
    pivot_risk = df.pivot_table(
        index="Month_Name",
        columns="day",
        values="Fire_Label",
        aggfunc="mean"
    ).reindex(["Tháng 6", "Tháng 7", "Tháng 8", "Tháng 9"])

    fig_heat = px.imshow(
        pivot_risk,
        labels=dict(x="Ngày trong tháng", y="Tháng", color="Mức độ rủi ro cháy"),
        x=[str(d) for d in pivot_risk.columns],
        y=pivot_risk.index,
        color_continuous_scale=[
            [0.0, "#10b981"],
            [0.5, "#f59e0b"],
            [1.0, "#ef4444"]
        ],
        aspect="auto"
    )
    fig_heat.update_layout(height=280, margin=dict(l=40, r=40, t=30, b=40))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
    📊 **Tóm tắt quy luật mùa vụ**:
    - **Tháng 6**: Giai đoạn đầu mùa khô, chỉ số ẩm thực bì tầng mặt còn tương đối, các đám cháy chỉ xuất hiện rải rác vào cuối tháng.
    - **Tháng 7 & 8**: Mùa cháy cao điểm toàn diện. Các đám cháy diễn ra liên tục hàng tuần, đặc biệt trong các đợt gió nóng khô Sirocco từ sa mạc Sahara thổi về.
    - **Tháng 9**: Các đợt mưa dông cuối mùa xuất hiện thường xuyên hơn, hạ nhiệt độ và kết thúc mùa cháy rừng tại Bắc Phi.
    """)
