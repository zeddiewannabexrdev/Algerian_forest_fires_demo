WEATHER_FEATURES = ["Temperature", "RH", "Ws", "Rain"]
FWI_FEATURES = ["FFMC", "DMC", "DC", "ISI", "BUI", "FWI"]
ALL_MODEL_FEATURES = WEATHER_FEATURES + FWI_FEATURES

# Vietnamese label mappings for UI presentation
FEATURE_NAMES_VI = {
    "Temperature": "Nhiệt độ (°C)",
    "RH": "Độ ẩm tương đối (%)",
    "Ws": "Tốc độ gió (km/h)",
    "Rain": "Lượng mưa (mm)",
    "FFMC": "Chỉ số mùn bề mặt (FFMC)",
    "DMC": "Chỉ số tầng hữu cơ trung bình (DMC)",
    "DC": "Chỉ số khô hạn tầng sâu (DC)",
    "ISI": "Tốc độ lan truyền lửa (ISI)",
    "BUI": "Tổng lượng vật liệu cháy (BUI)",
    "FWI": "Chỉ số thời tiết cháy rừng (FWI)",
}

FEATURE_RANGES = {
    "Temperature": {"min": 15.0, "max": 50.0, "default": 32.0, "step": 0.5, "unit": "°C"},
    "RH": {"min": 10.0, "max": 100.0, "default": 60.0, "step": 1.0, "unit": "%"},
    "Ws": {"min": 5.0, "max": 35.0, "default": 16.0, "step": 1.0, "unit": "km/h"},
    "Rain": {"min": 0.0, "max": 25.0, "default": 0.0, "step": 0.1, "unit": "mm"},
    "FFMC": {"min": 25.0, "max": 98.0, "default": 80.0, "step": 0.5, "unit": ""},
    "DMC": {"min": 0.5, "max": 70.0, "default": 12.0, "step": 0.5, "unit": ""},
    "DC": {"min": 5.0, "max": 230.0, "default": 45.0, "step": 1.0, "unit": ""},
    "ISI": {"min": 0.0, "max": 20.0, "default": 5.0, "step": 0.1, "unit": ""},
    "BUI": {"min": 1.0, "max": 70.0, "default": 16.0, "step": 0.5, "unit": ""},
    "FWI": {"min": 0.0, "max": 35.0, "default": 6.0, "step": 0.1, "unit": ""},
}

# Refined muted status colors
RISK_LEVELS = [
    {
        "name": "Cấp 1 - Thấp",
        "min_score": 0.0,
        "max_score": 0.25,
        "color": "#2e6f40",
        "badge": "AN TOÀN",
        "description": "Thực bì ẩm, ít khả năng phát sinh đám cháy. Hoạt động kiểm lâm duy trì thường xuyên.",
        "actions": [
            "Duy trì chế độ tuần tra bảo vệ rừng theo định kỳ.",
            "Tuyên truyền bảo vệ rừng cho dân cư vùng giáp ranh.",
            "Kiểm tra định kỳ trang thiết bị và bể chứa nước."
        ]
    },
    {
        "name": "Cấp 2 - Trung bình",
        "min_score": 0.25,
        "max_score": 0.50,
        "color": "#9a6a12",
        "badge": "CHÚ Ý",
        "description": "Thực bì bắt đầu khô kiệt. Nguy cơ bén lửa nếu gặp gió mạnh hoặc nguồn nhiệt bất cẩn.",
        "actions": [
            "Tăng tần suất tuần tra tại các khu vực thực bì dày, dễ bắt lửa.",
            "Kiểm soát nghiêm ngặt các hoạt động đốt dọn thực bì, nương rẫy.",
            "Kiểm tra sẵn sàng các nguồn nước và lối tiếp cận xe chữa cháy."
        ]
    },
    {
        "name": "Cấp 3 - Nguy hiểm",
        "min_score": 0.50,
        "max_score": 0.75,
        "color": "#b4431a",
        "badge": "NGUY HIỂM",
        "description": "Thời tiết khô nóng gay gắt. Đám cháy bùng phát nhanh và lan truyền diện rộng.",
        "actions": [
            "Lực lượng kiểm lâm trực 24/24 tại chòi canh và trạm gác cửa rừng.",
            "Nghiêm cấm người không có nhiệm vụ mang bật lửa, chất cháy vào rừng.",
            "Chuẩn bị sẵn sàng phương tiện cơ động và lực lượng cơ động tại chỗ."
        ]
    },
    {
        "name": "Cấp 4 - Cực kỳ nguy hiểm",
        "min_score": 0.75,
        "max_score": 1.00,
        "color": "#991b1b",
        "badge": "CỰC KỲ NGUY HIỂM",
        "description": "Hạn hán tích lũy ở mức báo động đỏ. Tốc độ lan tràn lửa cực lớn, nguy cơ thảm họa.",
        "actions": [
            "Ban bố tình trạng khẩn cấp, huy động hiệp đồng quân đội và công an.",
            "Bố trí xe bồn và máy bơm dã chiến tại các trục đường ranh cản lửa.",
            "Sơ tán người dân khỏi khu vực nguy cơ cao; sử dụng thiết bị bay quan trắc."
        ]
    }
]

CLIMATE_PRESETS = {
    "normal": {
        "title": "Thời tiết Mùa Hè Thông Thường",
        "desc": "Điều kiện nhiệt độ và độ ẩm trung bình mùa hè tại Algeria.",
        "delta": {"Temperature": 0.0, "RH": 0.0, "Ws": 0.0, "Rain": 0.0}
    },
    "heatwave": {
        "title": "Đợt Sóng Nhiệt Cực Đoan (El Niño)",
        "desc": "Nhiệt độ tăng +5°C, độ ẩm giảm -35%, gió nóng khô tăng +8 km/h.",
        "delta": {"Temperature": 5.0, "RH": -35.0, "Ws": 8.0, "Rain": 0.0}
    },
    "climate_change_2050": {
        "title": "Kịch Bản Biến Đổi Khí Hậu 2050 (IPCC RCP 8.5)",
        "desc": "Nhiệt độ nền tăng +3°C, độ ẩm giảm -15%, hạn hán kéo dài.",
        "delta": {"Temperature": 3.0, "RH": -15.0, "Ws": 4.0, "Rain": -1.0}
    },
    "flash_rain": {
        "title": "Mưa Dông Giải Nhiệt",
        "desc": "Mưa 10mm, nhiệt độ giảm -4°C, độ ẩm không khí tăng +40%.",
        "delta": {"Temperature": -4.0, "RH": 40.0, "Ws": -3.0, "Rain": 10.0}
    }
}


def get_theme_palette(is_dark: bool = False) -> dict:
    """Returns high-contrast color coordinates for Light or Dark theme mode."""
    if is_dark:
        return {
            "is_dark": True,
            "bg_app": "#0b0f19",
            "bg_card": "#131b2e",
            "bg_surface": "#1e293b",
            "border": "#2d3748",
            "border_accent": "#475569",
            "text_primary": "#f8fafc",
            "text_secondary": "#e2e8f0",
            "text_muted": "#94a3b8",
            "chart_paper": "#131b2e",
            "chart_plot": "#131b2e",
            "chart_grid": "#1e293b",
            "chart_text": "#f8fafc",
            "tag_bg": "#1e293b",
            "accent_line": "#38bdf8",
        }
    else:
        return {
            "is_dark": False,
            "bg_app": "#f8fafc",
            "bg_card": "#ffffff",
            "bg_surface": "#f1f5f9",
            "border": "#cbd5e1",
            "border_accent": "#94a3b8",
            "text_primary": "#090d16",
            "text_secondary": "#1e293b",
            "text_muted": "#475569",
            "chart_paper": "#ffffff",
            "chart_plot": "#ffffff",
            "chart_grid": "#e2e8f0",
            "chart_text": "#090d16",
            "tag_bg": "#f1f5f9",
            "accent_line": "#090d16",
        }
