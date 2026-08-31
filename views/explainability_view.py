import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import FEATURE_NAMES_VI


def render_explainability_view(df: pd.DataFrame, dt_model, rf_model, evaluator, palette: dict):
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

    st.markdown(f"<h4 style='font-family:{font_title}; color:{text_pri}; margin:0;'>GIẢI MÃ TRỌNG SỐ MÔI TRƯỜNG & ĐỐI CHIẾU THUẬT TOÁN</h4>", unsafe_allow_html=True)
    st.caption("Phân tích cơ chế ra quyết định của Decision Tree và Random Forest, bóc tách trọng số Gini và bộ luật điều kiện phân nhánh.")

    st.markdown(f"<div style='font-family: {font_title}; font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Hiệu Năng Đo Lường (Benchmark Matrix)</div>", unsafe_allow_html=True)
    if evaluator.metrics_summary is not None:
        st.dataframe(
            evaluator.metrics_summary,
            use_container_width=True,
            hide_index=True
        )

    col_roc, col_cm = st.columns([1, 1])
    with col_roc:
        st.plotly_chart(evaluator.plot_roc_curves_plotly(palette), use_container_width=True)
    with col_cm:
        st.plotly_chart(evaluator.plot_confusion_matrices_plotly(palette), use_container_width=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family: {font_title}; font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Trọng Số Đóng Góp Của Các Đặc Trưng (Feature Importance)</div>", unsafe_allow_html=True)

    df_comp_imp = evaluator.get_comparison_feature_importances()
    df_comp_imp["Feature_Name_VI"] = df_comp_imp["Feature"].map(lambda x: FEATURE_NAMES_VI.get(x, x))

    rf_bar_col = "#38bdf8" if is_dark else "#090d16"
    dt_bar_col = "#94a3b8" if is_dark else "#475569"

    fig_imp = go.Figure()
    fig_imp.add_trace(go.Bar(
        x=df_comp_imp["Feature_Name_VI"],
        y=df_comp_imp["DT_Percentage"],
        name="Decision Tree",
        marker_color=dt_bar_col,
        text=[f"{v:.1f}%" for v in df_comp_imp["DT_Percentage"]],
        textposition="outside",
        textfont=dict(family="Consolas, monospace", size=11, color=text_pri)
    ))
    fig_imp.add_trace(go.Bar(
        x=df_comp_imp["Feature_Name_VI"],
        y=df_comp_imp["RF_Percentage"],
        name="Random Forest",
        marker_color=rf_bar_col,
        text=[f"{v:.1f}%" for v in df_comp_imp["RF_Percentage"]],
        textposition="outside",
        textfont=dict(family="Consolas, monospace", size=11, color=text_pri)
    ))

    fig_imp.update_layout(
        barmode="group",
        xaxis=dict(title=dict(text="Thuộc tính", font=dict(color=text_pri, family=palette.get("font_title", "Montserrat, sans-serif"))), gridcolor=grid_col, tickfont=dict(color=text_sec, family=palette.get("font_body", "Lato, sans-serif"))),
        yaxis=dict(title=dict(text="Tỷ lệ trọng số (%)", font=dict(color=text_pri, family=palette.get("font_title", "Montserrat, sans-serif"))), gridcolor=grid_col, tickfont=dict(color=text_sec, family=palette.get("font_body", "Lato, sans-serif"))),
        height=360,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        font={"family": palette.get("font_body", "Lato, sans-serif"), "color": text_pri, "size": 12},
        margin=dict(l=30, r=30, t=20, b=60),
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.98, bgcolor=card_bg, bordercolor=border_col, borderwidth=1, font=dict(color=text_pri, family=palette.get("font_body", "Lato, sans-serif")))
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown(f"""
    <div style="border-left: 3px solid {border_col}; padding-left: 12px; font-size: 13px; color: {text_sec}; font-weight: 500; margin-top: 6px; font-family: {palette['font_body']};">
        PHÂN TÍCH TRỌNG SỐ: Chỉ số ISI (Initial Spread Index) chiếm tỷ trọng chi phối trong việc phân định ban đầu. Decision Tree tập trung phần lớn trọng số vào chỉ số này tại nút gốc do bản chất phân chia cục bộ tối ưu (greedy). Random Forest, nhờ kỹ thuật lấy mẫu ngẫu nhiên không gian thuộc tính tại mỗi phân nhánh (Feature Subsampling), phân phối tỷ trọng đồng đều hơn sang FFMC, FWI, DC và Nhiệt độ, nâng cao khả năng khái quát hóa khi gặp dữ liệu nhiễu.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-family: {font_title}; font-size: 13px; font-weight: 700; color: {text_pri}; text-transform: uppercase; margin-bottom: 8px; border-bottom: 1px solid {border_col}; padding-bottom: 4px;'>Cấu Trúc Cây Quyết Định & Hệ Thống Luật Suy Luận</div>", unsafe_allow_html=True)

    tab_diagram, tab_rules = st.tabs(["Sơ đồ Cây Quyết Định", "Danh sách Bộ Luật Phân Nhánh"])

    with tab_diagram:
        with st.spinner("Đang kết xuất sơ đồ cây..."):
            fig_tree = dt_model.plot_tree_diagram(palette=palette)
            st.pyplot(fig_tree, use_container_width=True)

    with tab_rules:
        rules_list = dt_model.export_rules_vi()
        df_rules = pd.DataFrame(rules_list)

        filter_type = st.radio(
            "Lọc quy luật theo kết quả:",
            options=["Tất cả", "Chỉ luật kích hoạt CHÁY", "Chỉ luật AN TOÀN"],
            horizontal=True,
            label_visibility="collapsed"
        )

        if "CHÁY" in filter_type:
            df_display = df_rules[df_rules["prediction"].str.contains("CHÁY")]
        elif "AN TOÀN" in filter_type:
            df_display = df_rules[df_rules["prediction"].str.contains("AN TOÀN")]
        else:
            df_display = df_rules

        for idx, row in df_display.iterrows():
            is_fire = "CHÁY" in row["prediction"]
            tag_border = "#ef4444" if is_fire else "#2e6f40"

            st.markdown(f"""
            <div style="background-color: {card_bg}; border: 1px solid {border_col}; border-left: 4px solid {tag_border}; border-radius: 4px; padding: 12px 16px; margin-bottom: 10px; font-family: {palette['font_body']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-family: {palette['font_title']}; font-weight: 700; color: {text_pri}; font-size: 14px;">QUY TẮC {idx + 1}: KẾT LUẬN {row['prediction']}</span>
                    <span style="font-family: Consolas, monospace; font-size: 12px; font-weight: 700; color: {text_pri}; background-color: {palette['bg_surface']}; border: 1px solid {border_col}; padding: 2px 8px; border-radius: 3px;">P = {row['fire_probability']:.1f}%</span>
                </div>
                <div style="font-family: Consolas, monospace; font-size: 13px; font-weight: 600; color: {text_pri}; background: {palette['bg_surface']}; padding: 8px 12px; border-radius: 3px; border: 1px solid {border_col};">
                    NẾU {row['condition_str']}
                </div>
                <div style="font-size: 12px; color: {text_sec}; margin-top: 6px; font-family: Consolas, monospace; font-weight: 600;">
                    Số mẫu thỏa mãn: {row['sample_count']} ngày | Mức tin cậy: {row['confidence']}
                </div>
            </div>
            """, unsafe_allow_html=True)
