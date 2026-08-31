import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import FWI_FEATURES, WEATHER_FEATURES, FEATURE_NAMES_VI


def render_regional_view(df: pd.DataFrame):
    st.markdown("### 🗺️ Phân Tích Đối Chiếu Khí Hậu & Rủi Ro Vùng Miền")
    st.caption("Khảo sát sự khác biệt về vi khí hậu, chỉ số FWI và tần suất phát hỏa giữa vùng duyên hải Bejaia và cao nguyên nội địa Sidi-Bel Abbes.")

    df_bej = df[df["Region"] == "Bejaia"]
    df_sidi = df[df["Region"] == "Sidi-Bel Abbes"]

    st.subheader("1. Tổng Quan Tương Quan Địa Lý & Tần Suất Cháy")

    bej_fires = int(df_bej["Fire_Label"].sum())
    sidi_fires = int(df_sidi["Fire_Label"].sum())
    bej_rate = (bej_fires / len(df_bej)) * 100
    sidi_rate = (sidi_fires / len(df_sidi)) * 100

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="Tỷ lệ cháy tại Bejaia (Ven biển)",
            value=f"{bej_rate:.1f}%",
            delta=f"{bej_fires}/{len(df_bej)} ngày quan trắc"
        )
    with col2:
        st.metric(
            label="Tỷ lệ cháy tại Sidi-Bel Abbes (Nội địa)",
            value=f"{sidi_rate:.1f}%",
            delta=f"{sidi_fires}/{len(df_sidi)} ngày quan trắc",
            delta_color="inverse"
        )
    with col3:
        st.metric(
            label="Nhiệt độ TB Bejaia vs Sidi",
            value=f"{df_bej['Temperature'].mean():.1f}°C vs {df_sidi['Temperature'].mean():.1f}°C",
            delta=f"Sidi cao hơn {df_sidi['Temperature'].mean() - df_bej['Temperature'].mean():.1f}°C"
        )
    with col4:
        st.metric(
            label="Độ ẩm TB Bejaia vs Sidi",
            value=f"{df_bej['RH'].mean():.1f}% vs {df_sidi['RH'].mean():.1f}%",
            delta=f"Sidi khô hơn {df_sidi['RH'].mean() - df_bej['RH'].mean():.1f}%",
            delta_color="inverse"
        )

    st.markdown("---")
    st.subheader("2. Biểu Đồ Mạng Nhện (Radar Chart): Hồ Sơ Vật Liệu Cháy FWI")
    st.caption("Chuẩn hóa min-max các chỉ số FWI để so sánh mức độ nhạy cảm cháy rừng toàn diện giữa hai vùng:")

    # Min-max normalization (0-100) for radar comparability
    radar_categories = FWI_FEATURES
    bej_fwi_norm = []
    sidi_fwi_norm = []

    for feat in radar_categories:
        min_v = df[feat].min()
        max_v = df[feat].max()
        val_bej = ((df_bej[feat].mean() - min_v) / (max_v - min_v)) * 100 if max_v > min_v else 0
        val_sidi = ((df_sidi[feat].mean() - min_v) / (max_v - min_v)) * 100 if max_v > min_v else 0
        bej_fwi_norm.append(val_bej)
        sidi_fwi_norm.append(val_sidi)

    # Close polar polygon loop
    radar_categories_closed = radar_categories + [radar_categories[0]]
    bej_closed = bej_fwi_norm + [bej_fwi_norm[0]]
    sidi_closed = sidi_fwi_norm + [sidi_fwi_norm[0]]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=bej_closed, theta=radar_categories_closed,
        fill="toself", name="Bejaia (Duyên hải Đông Bắc)",
        line=dict(color="#3b82f6", width=2.5),
        fillcolor="rgba(59, 130, 246, 0.25)"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=sidi_closed, theta=radar_categories_closed,
        fill="toself", name="Sidi-Bel Abbes (Nội địa Tây Bắc)",
        line=dict(color="#ef4444", width=2.5),
        fillcolor="rgba(239, 68, 68, 0.25)"
    ))

    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%")),
        showlegend=True,
        height=420,
        margin=dict(l=40, r=40, t=30, b=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")
    st.subheader("3. So Sánh Phân Phối Chi Tiết Từng Thông Số (Boxplot)")
    
    col_sel, _ = st.columns([2, 2])
    with col_sel:
        selected_param = st.selectbox(
            "Chọn thông số khí hậu để đối chiếu phân phối:",
            options=WEATHER_FEATURES + FWI_FEATURES,
            format_func=lambda x: FEATURE_NAMES_VI.get(x, x)
        )

    fig_box = px.box(
        df,
        x="Region",
        y=selected_param,
        color="Classes",
        color_discrete_map={"fire": "#ef4444", "not fire": "#10b981"},
        labels={"Region": "Khu vực", selected_param: FEATURE_NAMES_VI.get(selected_param, selected_param), "Classes": "Hiện trạng"},
        title=f"Phân phối {FEATURE_NAMES_VI.get(selected_param, selected_param)} giữa Bejaia và Sidi-Bel Abbes (theo trạng thái cháy)",
        points="all"
    )
    fig_box.update_layout(height=420, margin=dict(l=40, r=40, t=50, b=40))
    st.plotly_chart(fig_box, use_container_width=True)

    st.subheader("4. Tần Suất Ngày Cháy Theo Tháng Giữa 2 Vùng")
    
    monthly_summary = df.groupby(["Month_Name", "Region"])["Fire_Label"].agg(
        Total_Days="count",
        Fire_Days="sum"
    ).reset_index()
    monthly_summary["Fire_Percentage"] = (monthly_summary["Fire_Days"] / monthly_summary["Total_Days"]) * 100

    fig_bar = px.bar(
        monthly_summary,
        x="Month_Name",
        y="Fire_Days",
        color="Region",
        barmode="group",
        color_discrete_map={"Bejaia": "#3b82f6", "Sidi-Bel Abbes": "#f97316"},
        labels={"Month_Name": "Tháng", "Fire_Days": "Số ngày xảy ra cháy", "Region": "Vùng miền"},
        text="Fire_Days"
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(height=380, margin=dict(l=40, r=40, t=30, b=40))
    st.plotly_chart(fig_bar, use_container_width=True)

    st.info("""
    📌 **Kết luận đối chiếu vùng miền**:
    - **Sidi-Bel Abbes** có tỷ lệ bùng phát cháy vượt trội (**63.9%** so với **48.4%** của Bejaia). Nguyên nhân là do vị trí nội địa cao nguyên không được hưởng hơi ẩm điều hòa từ biển, dẫn đến độ ẩm tương đối thấp hơn và chỉ số hạn hán tầng sâu (DC) tích lũy cao hơn đáng kể.
    - **Bejaia** tuy có những ngày gió mạnh từ biển (Ws cao), nhưng độ ẩm không khí (RH) cao hơn giúp kìm hãm tốc độ khô kiệt của thảm mùn bổi bề mặt (FFMC).
    """)
