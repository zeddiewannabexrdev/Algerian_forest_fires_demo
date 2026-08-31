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

RISK_LEVELS = [
    {
        "name": "Cấp 1 - Thấp (An toàn)",
        "min_score": 0.0,
        "max_score": 0.25,
        "color": "#10b981",
        "badge": "AN TOÀN",
        "description": "Thực bì ẩm, ít khả năng phát sinh đám cháy. Hoạt động sinh hoạt bình thường.",
        "actions": [
            "Duy trì chế độ tuần tra thông thường.",
            "Tuyên truyền bảo vệ rừng định kỳ cho người dân.",
            "Kiểm tra trang thiết bị phòng chữa cháy."
        ]
    },
    {
        "name": "Cấp 2 - Trung bình (Chú ý)",
        "min_score": 0.25,
        "max_score": 0.50,
        "color": "#f59e0b",
        "badge": "CHÚ Ý",
        "description": "Thực bì bắt đầu khô kiệt, mồi lửa có thể bén nếu gặp gió mạnh.",
        "actions": [
            "Tăng cường tuần tra tại các khu vực rừng thông, tràm dễ bắt lửa.",
            "Khuyến cáo người dân không đốt nương rẫy, xử lý thực bì bừa bãi.",
            "Kiểm tra các bể nước dự trữ và nguồn nước tự nhiên."
        ]
    },
    {
        "name": "Cấp 3 - Nguy hiểm (Báo động)",
        "min_score": 0.50,
        "max_score": 0.75,
        "color": "#f97316",
        "badge": "NGUY HIỂM",
        "description": "Nguy cơ bùng phát cháy cao. Lửa dễ bắt và lan truyền nhanh.",
        "actions": [
            "Trực chiến 24/24h tại các trạm canh gác và chòi quan sát lửa rừng.",
            "Nghiêm cấm hoàn toàn hành vi mang lửa, chất nổ vào rừng.",
            "Sẵn sàng phương tiện cơ động và lực lượng phản ứng nhanh tại chỗ."
        ]
    },
    {
        "name": "Cấp 4 - Cực kỳ nguy hiểm (Khẩn cấp)",
        "min_score": 0.75,
        "max_score": 1.00,
        "color": "#ef4444",
        "badge": "CỰC KỲ NGUY HIỂM",
        "description": "Chỉ số khô hạn và lan truyền lửa ở mức cực đoan. Lửa bùng phát dữ dội.",
        "actions": [
            "Kích hoạt trạng thái khẩn cấp cấp tỉnh/vùng, huy động lực lượng liên ngành.",
            "Bố trí xe cứu hỏa cơ động ứng trực tại cửa rừng trọng điểm.",
            "Sơ tán người dân khỏi khu vực ranh giới rừng có nguy cơ cao.",
            "Áp dụng flycam/drone trinh sát phát hiện sớm tàn lửa và khói."
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
        "desc": "Nhiệt độ tăng vọt +5°C, độ ẩm giảm mạnh -35%, gió nóng khô tăng +8 km/h.",
        "delta": {"Temperature": 5.0, "RH": -35.0, "Ws": 8.0, "Rain": 0.0}
    },
    "climate_change_2050": {
        "title": "Kịch Bản Biến Đổi Khí Hậu 2050 (IPCC RCP 8.5)",
        "desc": "Nhiệt độ nền tăng +3°C, độ ẩm giảm -15%, hạn hán kéo dài và gió tăng nhẹ.",
        "delta": {"Temperature": 3.0, "RH": -15.0, "Ws": 4.0, "Rain": -1.0}
    },
    "flash_rain": {
        "title": "Mưa Dông Bất Chợt Giải Nhiệt",
        "desc": "Có mưa dông giải hạn 10mm, nhiệt độ giảm -4°C, độ ẩm không khí tăng vọt +40%.",
        "delta": {"Temperature": -4.0, "RH": 40.0, "Ws": -3.0, "Rain": 10.0}
    }
}
