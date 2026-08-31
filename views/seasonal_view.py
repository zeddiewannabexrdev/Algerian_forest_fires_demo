import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import FEATURE_NAMES_VI


def render_seasonal_view(df: pd.DataFrame, palette: dict):
    text_pri = palette["text_primary"]
    text_sec = palette["text_secondary"]
    border_col = palette["border"]
    card_bg = palette["bg_card"]
    paper_bg = palette["chart_paper"]
    plot_bg = palette["chart_plot"]
    grid_col = palette["chart_grid"]
    is_dark = palette["is_dark"]

    st.markdown(f"<h4 style='color:{text_pri}; margin:0;'>TRUY VẾT RỦI RO THEO MÙA VỤ & DIỄN BIẾN THỜI GIAN</h4>", unsafe_allow_html=True)
    st.caption("Giám sát chuỗi thời gian 4 tháng mùa hè (Tháng 6 - Tháng 9/2012), phân tích cơ chế tích lũy khô hạn và chu kỳ phát hỏa.")

    col_region, _ = st.columns([2, 2])
    with col_region:
        sel_region = st.selectbox(
            "Phạm vi phân tích:",
            options=["Toàn bộ Algeria (Cả 2 vùng)", "Bejaia (Ven biển)", "Sidi-Bel Abbes (Nội địa)"]
        )

    if "Bejaia" in sel_region:
        df_view = df[df["Region"] == "Bejaia"].copy()
    elif "Sidi" in sel_region:
        df_view = df[df["Region"] == "Sidi-Bel Abbes"].copy()
    else:
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

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Chuỗi Thời Gian Quan Trắc Liên Tục (Timeline)</div>", unsafe_allow_html=True)

    fig_time = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Nhiệt độ (°C) & Lượng mưa (mm)", "Chỉ số FWI & Ngày có cháy")
    )

    temp_color = "#38bdf8" if is_dark else "#090d16"
    rain_color = "#475569" if is_dark else "#64748b"
    fwi_color = "#cbd5e1" if is_dark else "#334155"
    fire_marker_color = "#ef4444" if is_dark else "#991b1b"

    fig_time.add_trace(
        go.Scatter(
            x=df_view["Date"], y=df_view["Temperature"],
            mode="lines",
            name="Nhiệt độ (°C)",
            line=dict(color=temp_color, width=2)
        ),
        row=1, col=1
    )
    fig_time.add_trace(
        go.Bar(
            x=df_view["Date"], y=df_view["Rain"],
            name="Lượng mưa (mm)",
            marker_color=rain_color,
            opacity=0.8
        ),
        row=1, col=1
    )

    fig_time.add_trace(
        go.Scatter(
            x=df_view["Date"], y=df_view["FWI"],
            mode="lines",
            name="Chỉ số FWI",
            line=dict(color=fwi_color, width=2)
        ),
        row=2, col=1
    )

    fire_days = df_view[df_view["Fire_Label"] == 1]
    fig_time.add_trace(
        go.Scatter(
            x=fire_days["Date"], y=fire_days["FWI"],
            mode="markers",
            name="Ngày Có Cháy",
            marker=dict(color=fire_marker_color, size=7, symbol="circle")
        ),
        row=2, col=1
    )

    fig_time.update_layout(
        height=440,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": "Segoe UI, Arial, sans-serif", "color": text_pri, "size": 12},
        margin=dict(l=30, r=30, t=30, b=30),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color=text_pri)),
        xaxis=dict(gridcolor=grid_col, tickfont=dict(color=text_sec)),
        yaxis=dict(gridcolor=grid_col, tickfont=dict(color=text_sec)),
        xaxis2=dict(gridcolor=grid_col, tickfont=dict(color=text_sec)),
        yaxis2=dict(gridcolor=grid_col, tickfont=dict(color=text_sec))
    )
    st.plotly_chart(fig_time, use_container_width=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Hiện Tượng Tích Lũy Khô Hạn Tầng Sâu (Drought Code)</div>", unsafe_allow_html=True)

    col_dc1, col_dc2 = st.columns([1.6, 1])

    with col_dc1:
        dc_colors = {
            "DC": "#ef4444" if is_dark else "#090d16",
            "DMC": "#f59e0b" if is_dark else "#475569",
            "BUI": "#38bdf8" if is_dark else "#64748b"
        }
        fig_dc = px.line(
            df_view,
            x="Date",
            y=["DC", "DMC", "BUI"],
            labels={"value": "Điểm số", "variable": "Chỉ số", "Date": "Ngày"},
            color_discrete_map=dc_colors
        )
        fig_dc.update_layout(
            height=300,
            paper_bgcolor=paper_bg,
            plot_bgcolor=plot_bg,
            font={"family": "Segoe UI, Arial, sans-serif", "color": text_pri, "size": 11},
            xaxis=dict(gridcolor=grid_col, title=dict(font=dict(color=text_pri)), tickfont=dict(color=text_sec)),
            yaxis=dict(gridcolor=grid_col, title=dict(font=dict(color=text_pri)), tickfont=dict(color=text_sec)),
            legend=dict(font=dict(color=text_pri)),
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_dc, use_container_width=True)

    with col_dc2:
        st.markdown(f"""
        <div style="border: 1px solid {border_col}; border-radius: 4px; padding: 16px; background-color: {card_bg}; height: 100%;">
            <div style="font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px;">Cơ chế tích lũy Tháng 8</div>
            <div style="font-size: 13px; color: {text_sec}; line-height: 1.7; font-weight: 500;">
                Chỉ số DC phản ánh lượng ẩm tầng hữu cơ sâu và rễ cây mục. Trái với tầng bề mặt (FFMC) vốn có thể hấp thụ ẩm trở lại sau một trận mưa rào nhỏ, tầng sâu cần nhiều tuần bốc hơi liên tục. Sang tháng 8, chỉ số DC đạt ngưỡng cực đại (>150), khiến các đám cháy nếu phát sinh sẽ ăn sâu xuống tầng rễ và duy trì nhiệt lượng rất lớn.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Ma Trận Lịch Rủi Ro Từng Ngày (Calendar Matrix)</div>", unsafe_allow_html=True)

    pivot_risk = df.pivot_table(
        index="Month_Name",
        columns="day",
        values="Fire_Label",
        aggfunc="mean"
    ).reindex(["Tháng 6", "Tháng 7", "Tháng 8", "Tháng 9"]).fillna(0)

    if is_dark:
        calendar_scale = [
            [0.0, "#131b2e"],
            [0.5, "#334155"],
            [1.0, "#ef4444"]
        ]
    else:
        calendar_scale = [
            [0.0, "#f8fafc"],
            [0.5, "#cbd5e1"],
            [1.0, "#090d16"]
        ]

    fig_heat = px.imshow(
        pivot_risk,
        labels=dict(x="Ngày", y="Tháng", color="Tần suất cháy"),
        x=[str(d) for d in pivot_risk.columns],
        y=pivot_risk.index,
        color_continuous_scale=calendar_scale,
        aspect="auto"
    )
    fig_heat.update_layout(
        height=240,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": "Segoe UI, Arial, sans-serif", "color": text_pri, "size": 12},
        xaxis=dict(tickfont=dict(color=text_pri)),
        yaxis=dict(tickfont=dict(color=text_pri)),
        coloraxis_colorbar=dict(tickfont=dict(color=text_pri), title=dict(font=dict(color=text_pri))),
        margin=dict(l=30, r=30, t=20, b=30)
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown(f"""
    <div style="border-left: 3px solid {border_col}; padding-left: 12px; font-size: 13px; color: {text_sec}; font-weight: 500; margin-top: 6px;">
        QUY LUẬT MÙA VỤ: Tháng 6 đóng vai trò giai đoạn chuyển tiếp, độ ẩm tầng sâu còn duy trì. Tháng 7 và 8 là cao điểm cháy diện rộng đồng bộ trên cả hai khu vực. Bước sang cuối tháng 9, lượng mưa xuất hiện giúp hạ nhiệt độ và giải tỏa trạng thái khô hạn.
    </div>
    """, unsafe_allow_html=True)
