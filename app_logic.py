# File: app_logic.py (Phiên bản v6.0 - Tích hợp tính năng mới)
from ultralytics import YOLO
from PIL import Image,ImageTk
import cv2
from collections import defaultdict
import json
import csv
from datetime import datetime
import os

# Không tải model nào lúc đầu
model = None 
current_confidence = 0.5

# Dashboard stats
detection_stats = {
    "total_detections": 0,
    "class_counts": defaultdict(int),
    "confidence_history": [],
    "detection_history": [],
    "timestamp_history": []
}

# Danh sách các model có sẵn và đường dẫn của chúng
# Mặc định: chỉ dùng model custom của bạn (models/best.pt). COCO đã được loại bỏ theo yêu cầu.
AVAILABLE_MODELS = {}

def switch_model(model_name):
    """Hàm để chuyển đổi giữa các model."""
    global model
    model_path = AVAILABLE_MODELS.get(model_name)
    # Nếu model_name là một đường dẫn file .pt trực tiếp
    if model_path is None and (os.path.exists(model_name) and model_name.lower().endswith('.pt')):
        model_path = model_name

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


def load_model_file(file_path, register=True):
    """Load một file model .pt trực tiếp và (tuỳ chọn) đăng ký vào AVAILABLE_MODELS.

    Trả về khoá (name) đã thêm vào AVAILABLE_MODELS khi thành công, hoặc False khi thất bại.
    """
    global model
    if not os.path.exists(file_path):
        print(f"File không tồn tại: {file_path}")
        return False

    try:
        print(f"Loading model from file: {file_path} ...")
        loaded = YOLO(file_path)
        model = loaded
        # Đăng ký model vào AVAILABLE_MODELS nếu yêu cầu
        if register:
            base = os.path.basename(file_path)
            name = os.path.splitext(base)[0]
            key = f"Custom ({name})"
            # ensure unique key
            suffix = 1
            orig_key = key
            while key in AVAILABLE_MODELS:
                suffix += 1
                key = f"{orig_key}-{suffix}"
            AVAILABLE_MODELS[key] = file_path
            print(f"Đăng ký model dưới tên: {key}")
            return key

        return True
    except Exception as e:
        print(f"Lỗi khi load model từ file: {e}")
        return False

def set_confidence_threshold(confidence):
    """Cập nhật confidence threshold"""
    global current_confidence
    current_confidence = max(0.1, min(0.9, confidence))

def get_model_info(model_key=None):
    """Trả về thông tin model hiện tại hoặc model được chỉ định bởi `model_key`.

    Trả về dict có các trường: name, classes, class_names, path, file_size
    """
    info = {"name": "Chưa tải model", "classes": 0, "class_names": [], "path": None, "file_size": None}

    # Nếu người gọi truyền model_key (là key trong AVAILABLE_MODELS), lấy path từ đó
    model_path = None
    if model_key:
        if model_key in AVAILABLE_MODELS:
            model_path = AVAILABLE_MODELS.get(model_key)
            info['name'] = model_key
    # Nếu không có key, nhưng có model đã load, cố lấy tên lớp từ object
    if model is not None:
        info['name'] = info.get('name') or 'Model hiện tại'
        try:
            if hasattr(model, 'names'):
                # model.names có thể là dict {id: name}
                names = model.names
                if isinstance(names, dict):
                    info['class_names'] = [v for k, v in sorted(names.items())]
                else:
                    info['class_names'] = list(names)
                info['classes'] = len(info['class_names'])
        except Exception:
            pass

    # Nếu có đường dẫn file (từ AVAILABLE_MODELS hoặc model_path), bổ sung kích thước
    if model_path:
        info['path'] = model_path
        try:
            if os.path.exists(model_path):
                info['file_size'] = f"{os.path.getsize(model_path) / (1024*1024):.2f} MB"
        except Exception:
            pass
    else:
        # Nếu không có model_path nhưng AVAILABLE_MODELS chỉ có một target, cố lấy từ đó
        try:
            if not model_path and AVAILABLE_MODELS:
                # if only one model registered, pick that path
                # otherwise leave path None
                if len(AVAILABLE_MODELS) == 1:
                    only_path = list(AVAILABLE_MODELS.values())[0]
                    info['path'] = only_path
                    if os.path.exists(only_path):
                        info['file_size'] = f"{os.path.getsize(only_path) / (1024*1024):.2f} MB"
        except Exception:
            pass

    return info

def get_detection_stats():
    """Trả về thống kê detection"""
    return detection_stats.copy()

def reset_stats():
    """Reset thống kê"""
    global detection_stats
    detection_stats = {
        "total_detections": 0,
        "class_counts": defaultdict(int),
        "confidence_history": [],
        "detection_history": [],
        "timestamp_history": []
    }

def export_stats_to_csv(filename):
    """Xuất thống kê ra CSV"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Object Detection Report', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
            writer.writerow([''])
            writer.writerow(['Total Detections:', detection_stats["total_detections"]])
            writer.writerow([''])
            writer.writerow(['Class', 'Count'])
            for class_name, count in detection_stats["class_counts"].items():
                writer.writerow([class_name, count])
        return True
    except Exception as e:
        print(f"Export CSV error: {e}")
        return False

def export_stats_to_json(filename):
    """Xuất thống kê ra JSON"""
    try:
        export_data = {
            "export_time": datetime.now().isoformat(),
            "total_detections": detection_stats["total_detections"],
            "class_counts": dict(detection_stats["class_counts"]),
            "confidence_history": detection_stats["confidence_history"],
            "detection_history": detection_stats["detection_history"],
            "timestamp_history": detection_stats["timestamp_history"]
        }
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Export JSON error: {e}")
        return False

# Khởi động với model mặc định
print("Khởi động: chỉ dùng model local. Kiểm tra models/best.pt ...")
if os.path.exists("models/best.pt"):
    # Đăng ký model custom mặc định
    AVAILABLE_MODELS.clear()
    AVAILABLE_MODELS["Custom (best)"] = "models/best.pt"
    if not switch_model("Custom (best)"):
        print("Không thể tải models/best.pt — kiểm tra file hoặc tải model mới bằng nút 'Load .pt'.")
else:
    # Không tự động tải COCO hay model từ mạng — người dùng sẽ load model bằng tay
    AVAILABLE_MODELS.clear()
    print("Chưa tìm thấy models/best.pt. Vui lòng đặt file 'best.pt' vào thư mục 'models/' hoặc dùng nút 'Load .pt' trong giao diện.")

def detect_objects_in_image(image_path):
    """Nhận diện đối tượng trong ảnh tĩnh"""
    global detection_stats
    
    try:
        results = model(image_path, conf=current_confidence)
        result = results[0]
        
        if len(result.boxes) == 0:
            return None, "Không phát hiện đối tượng nào trong ảnh.\nThử giảm confidence threshold."
        
        object_counts = defaultdict(int)
        detected_info = "--- ĐỐI TƯỢNG TRONG ẢNH ---\n"
        class_names = model.names
        
        boxes = result.boxes
        total_objects = len(boxes)
        confidences = []
        detected_objects = []
        
        for i in range(len(boxes)):
            class_id = int(boxes.cls[i].item())
            confidence = float(boxes.conf[i].item())
            class_name = class_names[class_id]
            object_counts[class_name] += 1
            confidences.append(confidence)
            detected_objects.append(class_name)
        
        # Cập nhật thống kê
        detection_stats["total_detections"] += total_objects
        for obj in detected_objects:
            detection_stats["class_counts"][obj] += 1
        
        if confidences:
            avg_conf = sum(confidences) / len(confidences)
            detection_stats["confidence_history"].append(avg_conf)
            detection_stats["detection_history"].append(total_objects)
            detection_stats["timestamp_history"].append(datetime.now().isoformat())
            
            # Giữ chỉ 100 records gần nhất
            if len(detection_stats["confidence_history"]) > 100:
                for key in ["confidence_history", "detection_history", "timestamp_history"]:
                    detection_stats[key] = detection_stats[key][-100:]
        
        detected_info += f"Tổng đối tượng: {total_objects}\n"
        detected_info += f"Confidence: {current_confidence}\n\n"
        
        for name, count in sorted(object_counts.items()):
            detected_info += f"• {name.capitalize()}: {count}\n"
            
        if confidences:
            avg_conf = sum(confidences) / len(confidences)
            detected_info += f"\n--- THỐNG KÊ ---\n"
            detected_info += f"Confidence TB: {avg_conf:.2f}\n"
            detected_info += f"Min: {min(confidences):.2f}\n"
            detected_info += f"Max: {max(confidences):.2f}"
        
        result_array_bgr = result.plot()
        result_array_rgb = result_array_bgr[..., ::-1]
        result_image = Image.fromarray(result_array_rgb)
        return result_image, detected_info
        
    except Exception as e:
        print(f"Lỗi logic AI (ảnh tĩnh): {e}")
        return None, f"Lỗi xử lý ảnh: {str(e)}"

def process_video_stream(source, image_label, data_label, app_instance):
    """Hàm xử lý video stream"""
    try:
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print(f"Lỗi: Không thể mở nguồn video từ source: {source}")
            app_instance.root.after(0, app_instance.stop_processing)
            return

        class_names = model.names
        track_history = defaultdict(lambda: [])
        counted_ids = set()
        object_counts_by_class = defaultdict(int)
        w, h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        line_y = h * 2 // 3
        
        while True:
            if not app_instance.is_processing_video: 
                break
            success, frame = cap.read()
            if not success: 
                break
                
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
                    if len(history) > 10: 
                        history.pop(0)
                    if len(history) > 1 and history[-2] < line_y and history[-1] >= line_y and track_id not in counted_ids:
                        counted_ids.add(track_id)
                        class_name = class_names[class_id]
                        object_counts_by_class[class_name] += 1
            
            detected_info = "--- BÁO CÁO GIÁM SÁT ---\n"
            total_count = sum(object_counts_by_class.values())
            detected_info += f"Tổng số đã qua: {total_count}\n\nChi tiết:\n"
            for name, count in sorted(object_counts_by_class.items()):
                 detected_info += f"- {name.capitalize()}: {count}\n"
            
            # Cập nhật text dashboard
            def update_text():
                try:
                    data_label.delete("1.0", "end")
                    data_label.insert("1.0", detected_info)
                except Exception as e:
                    print(f"Lỗi cập nhật text: {e}")
            
            app_instance.root.after(0, update_text)
            
            # Cập nhật ảnh - XÓA TEXT CŨ TRƯỚC
            img = Image.fromarray(annotated_frame[..., ::-1])
            img.thumbnail((750, 550))
            photo = ImageTk.PhotoImage(image=img)
            
            def update_image():
                try:
                    # XÓA TEXT CŨ và cập nhật ảnh mới
                    image_label.configure(text="", image=photo)
                    image_label.image = photo  # Giữ reference để tránh garbage collection
                except Exception as e:
                    print(f"Lỗi cập nhật ảnh: {e}")
            
            app_instance.root.after(0, update_image)
        
        # Tự động gọi hàm stop khi video kết thúc
        cap.release()
        app_instance.root.after(0, app_instance.stop_processing)
        print("Đã dừng xử lý video.")

    except Exception as e:
        print(f"Lỗi nghiêm trọng trong luồng AI (video): {e}")
        app_instance.root.after(0, app_instance.stop_processing)