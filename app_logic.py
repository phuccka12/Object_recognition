# File: app_logic.py (Phiên bản cuối cùng - Quản lý nhiều model)
from ultralytics import YOLO
from PIL import Image,ImageTk
import cv2
from collections import defaultdict

# Không tải model nào lúc đầu
model = None 

# Danh sách các model có sẵn và đường dẫn của chúng
AVAILABLE_MODELS = {
    "Tổng quát (COCO)": "yolov8n.pt",
    "Ẩm thực Việt (Custom)": "models/best.pt"
}

def switch_model(model_name):
    """Hàm để chuyển đổi giữa các model."""
    global model
    model_path = AVAILABLE_MODELS.get(model_name)
    if model_path:
        print(f"Đang chuyển sang model: {model_path}...")
        try:
            model = YOLO(model_path)
            print("Chuyển model thành công!")
            return True
        except Exception as e:
            print(f"Lỗi khi tải model: {e}")
            return False
    else:
        print(f"Lỗi: Không tìm thấy model tên là '{model_name}'")
        return False

# Khởi động với model mặc định khi bắt đầu
print("Đang tải model mặc định...")
switch_model("Tổng quát (COCO)")

# --- Các hàm xử lý giữ nguyên như cũ, không cần thay đổi ---
def detect_objects_in_image(image_path):
    # Code của hàm này y hệt phiên bản trước
    # ...
    try:
        results = model(image_path)
        result = results[0]
        object_counts = defaultdict(int)
        detected_info = "--- ĐỐI TƯỢNG TRONG ẢNH ---\n"
        class_names = model.names
        class_ids = result.boxes.cls.int().cpu().tolist()
        for class_id in class_ids:
            object_counts[class_names[class_id]] += 1
        for name, count in sorted(object_counts.items()):
            detected_info += f"- {name.capitalize()}: {count}\n"
        result_array_bgr = result.plot()
        result_array_rgb = result_array_bgr[..., ::-1]
        result_image = Image.fromarray(result_array_rgb)
        return result_image, detected_info
    except Exception as e:
        print(f"Lỗi logic AI (ảnh tĩnh): {e}")
        return None, "Lỗi xử lý ảnh."

def process_video_stream(source, image_label, data_label, app_instance):
    """
    Hàm được nâng cấp để chạy mượt mà trong một luồng riêng.
    """
    try:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"Lỗi: Không thể mở nguồn video từ source: {source}")
            app_instance.stop_processing() # Báo cho giao diện biết là đã dừng
            return

        # ... (toàn bộ vòng lặp while True giữ nguyên y hệt phiên bản trước)
        class_names = model.names
        track_history = defaultdict(lambda: [])
        counted_ids = set()
        object_counts_by_class = defaultdict(int)
        w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        line_y = h * 2 // 3
        while True:
            if not app_instance.is_processing_video: break
            success, frame = cap.read()
            if not success: break
            results = model.track(frame, persist=True, verbose=False)
            annotated_frame = results[0].plot()
            cv2.line(annotated_frame, (0, line_y), (w, line_y), (0, 0, 255), 2)
            if results[0].boxes.id is not None:
                boxes = results[0].boxes.xywh.cpu()
                track_ids = results[0].boxes.id.int().cpu().tolist()
                class_ids = results[0].boxes.cls.int().cpu().tolist()
                for box, track_id, class_id in zip(boxes, track_ids, class_ids):
                    x, y, _, _ = box
                    history = track_history[track_id]
                    history.append(y.item())
                    if len(history) > 10: history.pop(0)
                    if len(history) > 1 and history[-2] < line_y and history[-1] >= line_y and track_id not in counted_ids:
                        counted_ids.add(track_id)
                        class_name = class_names[class_id]
                        object_counts_by_class[class_name] += 1
            detected_info = "--- BÁO CÁO GIÁM SÁT ---\n"
            total_count = sum(object_counts_by_class.values())
            detected_info += f"Tổng số đã qua: {total_count}\n\nChi tiết:\n"
            for name, count in sorted(object_counts_by_class.items()):
                 detected_info += f"- {name.capitalize()}: {count}\n"
            data_label.configure(text=detected_info)
            img = Image.fromarray(annotated_frame[..., ::-1])
            img.thumbnail((750, 550))
            photo = ImageTk.PhotoImage(image=img)
            image_label.configure(image=photo)
            image_label.image = photo
            app_instance.root.update_idletasks()
        
        # Tự động gọi hàm stop khi video kết thúc
        cap.release()
        app_instance.stop_processing() 
        print("Đã dừng xử lý video.")

    except Exception as e:
        print(f"Lỗi nghiêm trọng trong luồng AI (video): {e}")
        # THÊM DÒNG NÀY: Đảm bảo giao diện được mở khóa dù có lỗi gì xảy ra
        app_instance.stop_processing()