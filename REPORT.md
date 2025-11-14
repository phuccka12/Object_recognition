# Báo cáo - Ứng dụng Nhận diện Đối tượng AI

## Mục tiêu
Xây dựng một ứng dụng desktop cho phép nhận diện, theo dõi và đếm đối tượng trong ảnh/video theo mô hình YOLOv8, có giao diện người dùng bằng CustomTkinter, hỗ trợ nạp model tùy chỉnh (.pt) và xuất báo cáo thống kê.

---

## Kiến trúc tổng quan
- Giao diện (UI): `main_app.py`, `ui_components.py` sử dụng `customtkinter` để tạo dashboard, điều khiển và panel.
- Logic AI: `app_logic.py` chứa phần load model (Ultralytics YOLO), chạy inference trên ảnh/khung hình, track đối tượng trong video và cập nhật thống kê.
- Xử lý ảnh: `image_utils.py`, `image_processor.py` (một số hàm xử lý ảnh tồn tại nhưng UI đã ẩn tính năng xử lý ảnh để báo cáo tập trung vào nhận diện).
- Models: folder `models/` chứa model .pt (ví dụ `best.pt` — model của đồ án). Ứng dụng chỉ sử dụng model local (offline) để tránh tải model từ mạng trong môi trường bảo mật.


## Luồng hoạt động chính
1. Khởi tạo: chương trình đọc `models/best.pt` (nếu tồn tại) và đăng ký dưới tên `Custom (best)`.
2. Người dùng khởi chạy ứng dụng, có thể:
   - Tải ảnh tĩnh và nhấn "Nhận diện" để chạy inference.
   - Chạy video hoặc webcam để xử lý theo thời gian thực (threaded) và hiển thị khung đã chú thích.
   - Load model mới bằng nút "📥 Load .pt" (nạp và đăng ký vào danh sách models).
   - Quản lý model bằng nút "⚙️ Quản lý" (đặt active, bỏ đăng ký, mở thư mục models).
3. Kết quả:
   - Ảnh/video được chú thích bằng bounding boxes và nhãn.
   - Thống kê được cập nhật trong `detection_stats` và hiển thị trong Dashboard.
   - Người dùng có thể xuất CSV/JSON từ Dashboard.


## Quyết định thiết kế (lý do và hiệu quả)
- Chỉ dùng model local (offline): đảm bảo reproducibility, an toàn cho dữ liệu và tuân thủ yêu cầu không gọi API ngoài (Roboflow/Cloud).
- Tách UI và logic AI: `main_app.py` (view/controller) vs `app_logic.py` (model/service) giúp dễ kiểm thử và bảo trì.
- Giao diện đơn giản, loại bỏ điều chỉnh ảnh trực tiếp để tập trung vào chức năng chính (nhận diện và thống kê).
- Bật `pack_propagate` và để `image_frame` expand giúp giao diện hiển thị ảnh rõ ràng trên các kích thước màn hình khác nhau.


## Hạn chế và hướng cải tiến
- Hiện chưa có cơ chế rollback khi unregister model — có thể thêm confirm dialog và lưu snapshot.
- Chưa có UI để chỉnh threshold confidence — có thể thêm lại trong phần quản lý nếu cần.
- Chưa tự động validate schema nhãn giữa nhiều model.
- Nếu cần, có thể thêm chức năng kiểm thử tự động (unit tests cho app_logic) để đảm bảo pipeline inference ổn định.


## Hướng dẫn sử dụng (tóm tắt)
1. Đặt file model `best.pt` của bạn vào thư mục `models/`.
2. Chạy ứng dụng:
```
python main_app.py
```
3. Sử dụng nút "📁 Tải Ảnh" để tải ảnh, sau đó nhấn "🎯 Nhận diện".
4. Dùng "📥 Load .pt" để nạp model khác nếu cần.
5. Mở "⚙️ Quản lý" để đặt model active hoặc bỏ đăng ký.
6. Xuất báo cáo bằng Dashboard (Export CSV / JSON).


## Kiểm thử & Xác nhận
- Đã kiểm tra: ứng dụng khởi động khi `models/best.pt` có mặt; combobox model cập nhật khi load model mới.
- Đã sửa: lỗi "cannot write mode RGBA as JPEG" bằng cách lưu PNG cho ảnh có alpha channel.
- Đã loại bỏ tham chiếu đến COCO để đảm bảo app chỉ dùng dữ liệu model cục bộ.


## Tệp đáng chú ý trong repo
- `main_app.py` - giao diện chính và điều khiển
- `app_logic.py` - logic load model, inference, track, stats
- `ui_components.py` - panel dashboard và advanced features
- `models/best.pt` - model custom (nếu có)
- `REPORT.md` - file này


## Ghi chú cho người chấm/báo cáo
- Nếu cần, tôi có thể chuyển phần phân tích này sang `REPORT.pdf` hoặc bổ sung các biểu đồ và ảnh chụp màn hình từ kết quả chạy để minh họa.
- Tôi cũng có thể thêm phần code snippet ngắn minh họa cách inference (ví dụ: dùng `ultralytics.YOLO` để kiểm tra classes của model).


---

Nếu bạn muốn tôi mở rộng phần phân tích (ví dụ: thêm biểu đồ so sánh precision/recall, trình tự pipeline inference, ảnh minh họa đầu-cuối, hoặc phần test-case cụ thể), nói tôi biết cụ thể bạn muốn thêm gì.