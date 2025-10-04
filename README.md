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