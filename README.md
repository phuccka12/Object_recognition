# 🚀 AI Object Detection Studio v6.1

Ứng dụng nhận diện đối tượng AI với giao diện thân thiện, hỗ trợ xử lý ảnh, video và webcam real-time.

## 📋 Yêu cầu hệ thống

- **Python**: 3.8+ (khuyến nghị 3.11)
- **RAM**: Tối thiểu 4GB (khuyến nghị 8GB+)
- **GPU**: Tùy chọn (CUDA để tăng tốc)
- **Webcam**: Tùy chọn (cho tính năng real-time)

## 🛠️ Cài đặt nhanh

### Cách 1: Tự động (Windows)
```bash
# Chạy file batch
install.bat
```

### Cách 2: Thủ công
```bash
# Clone hoặc download project
# Mở terminal trong thư mục project

# Cài đặt dependencies
pip install -r requirements.txt

# Hoặc chạy setup script
python setup.py
```

### Cách 3: Virtual Environment (Khuyến nghị)
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt (Windows)
venv\Scripts\activate

# Kích hoạt (Linux/Mac)
source venv/bin/activate

# Cài đặt packages
pip install -r requirements.txt
```

## 🎯 Chạy ứng dụng

```bash
python main_app.py
```

## 📁 Cấu trúc thư mục

```
Object_recognition/
├── main_app.py          # File chính
├── app_logic.py         # Logic AI
├── ui_components.py     # GUI components
├── image_utils.py       # Image processing
├── requirements.txt     # Dependencies
├── models/             # Thư mục models
│   └── best.pt         # Custom model (nếu có)
└── README.md           # Hướng dẫn này
```

## 🔧 Các tính năng

- ✅ **Multi-model support**: COCO + Custom models
- ✅ **Image processing**: Brightness, Contrast, Filters
- ✅ **Real-time detection**: Webcam + Video files
- ✅ **Object tracking**: Đếm objects qua counting line
- ✅ **Statistics dashboard**: Real-time stats
- ✅ **Export data**: CSV + JSON reports
- ✅ **Batch processing**: Multiple images
- ✅ **Modern UI**: CustomTkinter interface

## 🐛 Troubleshooting

### Lỗi import modules
```bash
pip install --upgrade ultralytics customtkinter
```

### Lỗi CUDA (GPU)
```bash
# Cài đặt CPU-only version
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### Lỗi webcam không mở
- Kiểm tra camera permissions
- Thử đổi camera index (0, 1, 2...)
- Đóng các app khác đang dùng camera

## 👥 Hỗ trợ

- **Issues**: Báo bug qua GitHub Issues
- **Email**: support@example.com
- **Docs**: Xem code comments chi tiết

## 📄 License

MIT License - Free to use and modify
