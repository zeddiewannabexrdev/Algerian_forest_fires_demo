import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import FWI_FEATURES, WEATHER_FEATURES, FEATURE_NAMES_VI


def render_regional_view(df: pd.DataFrame, palette: dict):
    text_pri = palette["text_primary"]
    text_sec = palette["text_secondary"]
    border_col = palette["border"]
    card_bg = palette["bg_card"]
    paper_bg = palette["chart_paper"]
    plot_bg = palette["chart_plot"]
    grid_col = palette["chart_grid"]
    is_dark = palette["is_dark"]

    st.markdown(f"<h4 style='color:{text_pri}; margin:0;'>PHÂN TÍCH ĐỐI CHIẾU VÙNG MIỀN</h4>", unsafe_allow_html=True)
    st.caption("So sánh tương quan vi khí hậu và tần suất bắt lửa giữa vùng duyên hải Bejaia và cao nguyên nội địa Sidi-Bel Abbes.")

    df_bej = df[df["Region"] == "Bejaia"]
    df_sidi = df[df["Region"] == "Sidi-Bel Abbes"]

    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Chỉ Số Quan Trắc Tổng Quan Theo Địa Giới</div>", unsafe_allow_html=True)

    bej_fires = int(df_bej["Fire_Label"].sum())
    sidi_fires = int(df_sidi["Fire_Label"].sum())
    bej_rate = (bej_fires / len(df_bej)) * 100
    sidi_rate = (sidi_fires / len(df_sidi)) * 100

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div style="border: 1px solid {border_col}; border-radius: 4px; padding: 12px 14px; background: {card_bg};">
            <div style="font-size: 12px; font-weight: 700; color: {text_sec}; text-transform: uppercase;">Tỷ lệ cháy (Bejaia)</div>
            <div style="font-size: 22px; font-family: Consolas, monospace; font-weight: 700; color: {text_pri}; margin-top: 2px;">{bej_rate:.1f}%</div>
            <div style="font-size: 12px; color: {text_sec}; font-weight: 600; font-family: Consolas, monospace;">{bej_fires}/{len(df_bej)} ngày quan trắc</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        fire_col = "#ef4444" if is_dark else "#991b1b"
        st.markdown(f"""
        <div style="border: 1px solid {border_col}; border-radius: 4px; padding: 12px 14px; background: {card_bg};">
            <div style="font-size: 12px; font-weight: 700; color: {text_sec}; text-transform: uppercase;">Tỷ lệ cháy (Sidi-Bel Abbes)</div>
            <div style="font-size: 22px; font-family: Consolas, monospace; font-weight: 700; color: {fire_col}; margin-top: 2px;">{sidi_rate:.1f}%</div>
            <div style="font-size: 12px; color: {text_sec}; font-weight: 600; font-family: Consolas, monospace;">{sidi_fires}/{len(df_sidi)} ngày quan trắc</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div style="border: 1px solid {border_col}; border-radius: 4px; padding: 12px 14px; background: {card_bg};">
            <div style="font-size: 12px; font-weight: 700; color: {text_sec}; text-transform: uppercase;">Nhiệt độ TB (Bejaia vs Sidi)</div>
            <div style="font-size: 18px; font-family: Consolas, monospace; font-weight: 700; color: {text_pri}; margin-top: 2px;">{df_bej['Temperature'].mean():.1f}°C / {df_sidi['Temperature'].mean():.1f}°C</div>
            <div style="font-size: 12px; color: {text_sec}; font-weight: 600; font-family: Consolas, monospace;">Chênh lệch: +{df_sidi['Temperature'].mean() - df_bej['Temperature'].mean():.1f}°C</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div style="border: 1px solid {border_col}; border-radius: 4px; padding: 12px 14px; background: {card_bg};">
            <div style="font-size: 12px; font-weight: 700; color: {text_sec}; text-transform: uppercase;">Độ ẩm TB (Bejaia vs Sidi)</div>
            <div style="font-size: 18px; font-family: Consolas, monospace; font-weight: 700; color: {text_pri}; margin-top: 2px;">{df_bej['RH'].mean():.1f}% / {df_sidi['RH'].mean():.1f}%</div>
            <div style="font-size: 12px; color: {text_sec}; font-weight: 600; font-family: Consolas, monospace;">Chênh lệch: -{df_bej['RH'].mean() - df_sidi['RH'].mean():.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Hồ Sơ Chuẩn Hóa Các Chỉ Số FWI (Radar Profile)</div>", unsafe_allow_html=True)

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

    radar_categories_closed = radar_categories + [radar_categories[0]]
    bej_closed = bej_fwi_norm + [bej_fwi_norm[0]]
    sidi_closed = sidi_fwi_norm + [sidi_fwi_norm[0]]

    bej_radar_color = "#94a3b8" if is_dark else "#475569"
    sidi_radar_color = "#38bdf8" if is_dark else "#090d16"
    sidi_fill = "rgba(56, 189, 248, 0.22)" if is_dark else "rgba(9, 13, 22, 0.22)"

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=bej_closed, theta=radar_categories_closed,
        fill="toself", name="Bejaia (Duyên hải Đông Bắc)",
        line=dict(color=bej_radar_color, width=2),
        fillcolor="rgba(148, 163, 184, 0.18)"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=sidi_closed, theta=radar_categories_closed,
        fill="toself", name="Sidi-Bel Abbes (Nội địa Tây Bắc)",
        line=dict(color=sidi_radar_color, width=2.5),
        fillcolor=sidi_fill
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], ticksuffix="%", tickfont=dict(size=10, color=text_sec, family="Consolas, monospace"), gridcolor=grid_col),
            angularaxis=dict(gridcolor=grid_col, tickfont=dict(size=11, color=text_pri, family="Segoe UI, sans-serif")),
            bgcolor=plot_bg
        ),
        showlegend=True,
        height=360,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": "Segoe UI, Arial, sans-serif", "color": text_pri, "size": 12},
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.98, bgcolor=card_bg, bordercolor=border_col, borderwidth=1, font=dict(color=text_pri)),
        margin=dict(l=30, r=30, t=20, b=30)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Phân Bố Tham Số Khí Tượng Chi Tiết (Boxplot)</div>", unsafe_allow_html=True)
    
    col_sel, _ = st.columns([2, 2])
    with col_sel:
        selected_param = st.selectbox(
            "Tham số khảo sát:",
            options=WEATHER_FEATURES + FWI_FEATURES,
            format_func=lambda x: FEATURE_NAMES_VI.get(x, x),
            label_visibility="collapsed"
        )

    box_fire_col = "#ef4444" if is_dark else "#090d16"
    box_notfire_col = "#38bdf8" if is_dark else "#64748b"

    fig_box = px.box(
        df,
        x="Region",
        y=selected_param,
        color="Classes",
        color_discrete_map={"fire": box_fire_col, "not fire": box_notfire_col},
        labels={"Region": "Khu vực", selected_param: FEATURE_NAMES_VI.get(selected_param, selected_param), "Classes": "Hiện trạng"},
        points="all"
    )
    fig_box.update_layout(
        height=360,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": "Segoe UI, Arial, sans-serif", "color": text_pri, "size": 12},
        xaxis=dict(gridcolor=grid_col, title=dict(font=dict(color=text_pri)), tickfont=dict(color=text_sec)),
        yaxis=dict(gridcolor=grid_col, title=dict(font=dict(color=text_pri)), tickfont=dict(color=text_sec)),
        legend=dict(font=dict(color=text_pri)),
        margin=dict(l=30, r=30, t=20, b=30)
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Tần Suất Số Ngày Cháy Theo Từng Tháng</div>", unsafe_allow_html=True)
    
    monthly_summary = df.groupby(["Month_Name", "Region"])["Fire_Label"].agg(
        Total_Days="count",
        Fire_Days="sum"
    ).reset_index()
    monthly_summary["Fire_Percentage"] = (monthly_summary["Fire_Days"] / monthly_summary["Total_Days"]) * 100

    bar_bej_col = "#64748b" if is_dark else "#475569"
    bar_sidi_col = "#38bdf8" if is_dark else "#090d16"

    fig_bar = px.bar(
        monthly_summary,
        x="Month_Name",
        y="Fire_Days",
        color="Region",
        barmode="group",
        color_discrete_map={"Bejaia": bar_bej_col, "Sidi-Bel Abbes": bar_sidi_col},
        labels={"Month_Name": "Tháng", "Fire_Days": "Số ngày cháy", "Region": "Vùng"},
        text="Fire_Days"
    )
    fig_bar.update_traces(textposition="outside", textfont=dict(family="Consolas, monospace", size=12, color=text_pri))
    fig_bar.update_layout(
        height=320,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": "Segoe UI, Arial, sans-serif", "color": text_pri, "size": 12},
        xaxis=dict(gridcolor=grid_col, title=dict(font=dict(color=text_pri)), tickfont=dict(color=text_sec)),
        yaxis=dict(gridcolor=grid_col, title=dict(font=dict(color=text_pri)), tickfont=dict(color=text_sec)),
        legend=dict(font=dict(color=text_pri)),
        margin=dict(l=30, r=30, t=20, b=30)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown(f"""
    <div style="border-left: 3px solid {border_col}; padding-left: 12px; font-size: 13px; color: {text_sec}; font-weight: 500; margin-top: 6px;">
        KẾT LUẬN QUAN TRẮC: Sidi-Bel Abbes có tỷ lệ bùng phát cháy 63.9% (so với 48.4% tại Bejaia). Vị trí nội địa cao nguyên thiếu hơi ẩm điều hòa từ Địa Trung Hải khiến độ ẩm tương đối thấp hơn và chỉ số khô hạn tầng sâu (DC) tích lũy nhanh hơn. Tại Bejaia, độ ẩm nền cao hơn giúp kìm hãm đà bốc hơi của thảm mục phủ mặt đất.
    </div>
    """, unsafe_allow_html=True)
