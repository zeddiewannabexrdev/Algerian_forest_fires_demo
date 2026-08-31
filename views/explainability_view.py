import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import FEATURE_NAMES_VI


def render_explainability_view(df: pd.DataFrame, dt_model, rf_model, evaluator):
    st.markdown("### 🧠 Giải Mã Trọng Số Môi Trường & So Sánh 2 Thuật Toán (Explainable AI)")
    st.caption("Khám phá cơ chế quyết định nội tại của Cây Quyết Định (Decision Tree) và Rừng Ngẫu Nhiên (Random Forest), bóc tách trọng số đóng góp của từng yếu tố khí tượng.")

    st.subheader("1. Bảng Đối Chiếu Hiệu Năng (Model Benchmark)")
    if evaluator.metrics_summary is not None:
        st.dataframe(
            evaluator.metrics_summary,
            use_container_width=True,
            hide_index=True
        )

    col_roc, col_cm = st.columns([1, 1])
    with col_roc:
        st.plotly_chart(evaluator.plot_roc_curves_plotly(), use_container_width=True)
    with col_cm:
        st.plotly_chart(evaluator.plot_confusion_matrices_plotly(), use_container_width=True)

    st.markdown("---")
    st.subheader("2. Giải Mã Trọng Số Đóng Góp Của Từng Yếu Tố Môi Trường")
    st.caption("So sánh tỷ lệ đóng góp (%) của từng đặc trưng dựa trên độ giảm chỉ số vẩn đục Gini (Mean Decrease Impurity):")

    df_comp_imp = evaluator.get_comparison_feature_importances()
    df_comp_imp["Feature_Name_VI"] = df_comp_imp["Feature"].map(lambda x: FEATURE_NAMES_VI.get(x, x))

    fig_imp = go.Figure()
    fig_imp.add_trace(go.Bar(
        x=df_comp_imp["Feature_Name_VI"],
        y=df_comp_imp["DT_Percentage"],
        name="Decision Tree (Cây đơn lẻ)",
        marker_color="#3b82f6",
        text=[f"{v:.1f}%" for v in df_comp_imp["DT_Percentage"]],
        textposition="outside"
    ))
    fig_imp.add_trace(go.Bar(
        x=df_comp_imp["Feature_Name_VI"],
        y=df_comp_imp["RF_Percentage"],
        name="Random Forest (100 Cây kết hợp)",
        marker_color="#10b981",
        text=[f"{v:.1f}%" for v in df_comp_imp["RF_Percentage"]],
        textposition="outside"
    ))

    fig_imp.update_layout(
        barmode="group",
        xaxis_title="Yếu tố Môi trường / Chỉ số FWI",
        yaxis_title="Trọng số đóng góp (%)",
        height=420,
        margin=dict(l=40, r=40, t=30, b=80),
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.98)
    )
    st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("""
    💡 **Bình luận chuyên sâu về trọng số môi trường**:
    - **ISI (Initial Spread Index - Tốc độ lan truyền lửa)** là yếu tố quyết định số 1 trong cả 2 thuật toán. ISI là sự kết hợp trực tiếp giữa gió và độ ẩm mùn tầng mặt (FFMC), thể hiện tốc độ lửa có thể bùng phát ngay khi bắt mồi.
    - **Sự khác biệt cốt lõi**:
      - **Decision Tree** có tính chất "tham lam" (greedy) nên dồn hầu như toàn bộ trọng số (**>90%**) vào `ISI` ngay tại nút gốc (root node).
      - **Random Forest** nhờ cơ chế lấy mẫu ngẫu nhiên tập thuộc tính (Feature Subsampling) tại mỗi lần rẽ nhánh nên phân bổ đều trọng số sang cả `FFMC`, `FWI`, `DC`, `DMC`, và `Nhiệt độ`. Điều này giúp mô hình chống chịu cực tốt khi dữ liệu thực địa bị thiếu hụt một vài chỉ số.
    """)

    st.markdown("---")
    st.subheader("3. Trực Quan Hóa Cây Quyết Định & Bộ Luật Rẽ Nhánh (Decision Rules)")
    st.caption("Cây quyết định cho phép 'mở hộp đen' mô hình học máy thành các quy luật điều kiện If-Else tường minh 100%:")

    tab_diagram, tab_rules = st.tabs(["🌳 Sơ Đồ Cây Quyết Định (Tree Diagram)", "📜 Danh Sách Bộ Luật If-Else Tiếng Việt"])

    with tab_diagram:
        with st.spinner("Đang kết xuất sơ đồ cây..."):
            fig_tree = dt_model.plot_tree_diagram()
            st.pyplot(fig_tree, use_container_width=True)

    with tab_rules:
        rules_list = dt_model.export_rules_vi()
        df_rules = pd.DataFrame(rules_list)

        filter_type = st.radio(
            "Lọc các quy luật theo kết quả dự báo:",
            options=["Tất cả luật", "Chỉ hiển thị luật kích hoạt CHÁY", "Chỉ hiển thị luật AN TOÀN"],
            horizontal=True
        )

        if "CHÁY" in filter_type:
            df_display = df_rules[df_rules["prediction"].str.contains("CHÁY")]
        elif "AN TOÀN" in filter_type:
            df_display = df_rules[df_rules["prediction"].str.contains("AN TOÀN")]
        else:
            df_display = df_rules

        for idx, row in df_display.iterrows():
            is_fire = "CHÁY" in row["prediction"]
            card_color = "#fef2f2" if is_fire else "#f0fdf4"
            border_color = "#ef4444" if is_fire else "#10b981"
            badge_color = "#b91c1c" if is_fire else "#15803d"

            st.markdown(f"""
            <div style="background-color: {card_color}; border-left: 5px solid {border_color}; border-radius: 6px; padding: 12px 16px; margin-bottom: 10px;">
                <div style="font-weight: bold; color: {badge_color}; font-size: 15px; margin-bottom: 5px;">
                    ▶ Luật #{idx + 1}: KẾT LUẬN {row['prediction']} (Xác suất: {row['fire_probability']:.1f}%)
                </div>
                <div style="font-family: monospace; font-size: 13px; color: #1e293b; background: white; padding: 6px 10px; border-radius: 4px; border: 1px solid #e2e8f0;">
                    <b>NẾU</b> {row['condition_str']}
                </div>
                <div style="font-size: 12px; color: #64748b; margin-top: 6px;">
                    Số mẫu lịch sử thỏa mãn: <b>{row['sample_count']} ngày</b> | Độ tin cậy: <b>{row['confidence']}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
