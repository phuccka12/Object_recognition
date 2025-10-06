<<<<<<< HEAD
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
=======
# Trạm Phân Tích AI Đa Năng (v5.2)

Đây là một đồ án môn học xây dựng ứng dụng Desktop cho phép nhận diện, theo dõi và đếm đối tượng trong ảnh và video thời gian thực bằng mô hình YOLOv8.

## Tính năng chính
- Nhận diện đối tượng trên ảnh tĩnh.
- Xử lý và nhận diện đối tượng trong video từ file.
- Xử lý và nhận diện đối tượng từ webcam thời gian thực.
- Hệ thống đếm đối tượng thông minh khi vượt qua ranh giới ảo.
- Hỗ trợ đa mô hình: Chuyển đổi giữa model COCO chung và model đã được huấn luyện tùy chỉnh.
- Giao diện hiện đại, mượt mà (CustomTkinter) và không bị treo (Multi-threading).

## Công nghệ sử dụng
- Python 3.x
- Ultralytics YOLOv8
- OpenCV
- CustomTkinter & Pillow
- Roboflow (để quản lý dataset)
- Google Colab (để huấn luyện)

## Hướng dẫn Cài đặt & Chạy
1. Clone repository này về máy:
   ```bash
   git clone [https://github.com/TEN_CUA_BAN/TEN_REPO.git](https://github.com/TEN_CUA_BAN/TEN_REPO.git)
   cd TEN_REPO
   ```
2. Tạo và kích hoạt môi trường ảo:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   # source venv/bin/activate
   ```
3. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
4. **(Quan trọng)** Để sử dụng model tùy chỉnh, hãy tạo thư mục `models` và đặt file `best.pt` của bạn vào đó.

5. Chạy ứng dụng:
   ```bash
   python main_app.py
   ```
>>>>>>> 07cec74f484f4692e1662607a87e4c11f7476393
