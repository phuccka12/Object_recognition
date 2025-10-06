# File: dashboard.py - Quản lý Dashboard và Thống kê
import customtkinter as ctk
from datetime import datetime
from collections import defaultdict
import json
import csv

class DashboardManager:
    def __init__(self):
        self.stats = {
            "total_detections": 0,
            "class_counts": defaultdict(int),
            "confidence_history": [],
            "detection_history": [],
            "timestamp_history": []
        }
    
    def update_stats(self, detected_objects, confidences):
        """Cập nhật thống kê từ kết quả detection"""
        self.stats["total_detections"] += len(detected_objects)
        
        for obj in detected_objects:
            self.stats["class_counts"][obj] += 1
        
        if confidences:
            avg_conf = sum(confidences) / len(confidences)
            self.stats["confidence_history"].append(avg_conf)
            self.stats["detection_history"].append(len(detected_objects))
            self.stats["timestamp_history"].append(datetime.now().isoformat())
            
            # Giữ chỉ 100 records gần nhất
            if len(self.stats["confidence_history"]) > 100:
                for key in ["confidence_history", "detection_history", "timestamp_history"]:
                    self.stats[key] = self.stats[key][-100:]
    
    def get_stats(self):
        """Trả về thống kê hiện tại"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset thống kê"""
        self.stats = {
            "total_detections": 0,
            "class_counts": defaultdict(int),
            "confidence_history": [],
            "detection_history": [],
            "timestamp_history": []
        }
    
    def export_to_csv(self, filename):
        """Xuất thống kê ra CSV"""
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Object Detection Report', f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
                writer.writerow([''])
                writer.writerow(['Total Detections:', self.stats["total_detections"]])
                writer.writerow([''])
                writer.writerow(['Class', 'Count'])
                for class_name, count in self.stats["class_counts"].items():
                    writer.writerow([class_name, count])
            return True
        except Exception as e:
            print(f"Export CSV error: {e}")
            return False
    
    def export_to_json(self, filename):
        """Xuất thống kê ra JSON"""
        try:
            export_data = {
                "export_time": datetime.now().isoformat(),
                "total_detections": self.stats["total_detections"],
                "class_counts": dict(self.stats["class_counts"]),
                "confidence_history": self.stats["confidence_history"],
                "detection_history": self.stats["detection_history"],
                "timestamp_history": self.stats["timestamp_history"]
            }
            
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Export JSON error: {e}")
            return False

def create_dashboard_frame(parent_frame, dashboard_manager):
    """Tạo frame dashboard"""
    # Title
    title = ctk.CTkLabel(parent_frame, text="📊 DASHBOARD", font=ctk.CTkFont(size=16, weight="bold"))
    title.pack(pady=10)
    
    # Stats display
    stats_frame = ctk.CTkFrame(parent_frame, height=200)
    stats_frame.pack(fill=ctk.X, padx=10, pady=5)
    stats_frame.pack_propagate(False)
    
    stats_text = ctk.CTkTextbox(stats_frame, height=180, font=ctk.CTkFont(family="Consolas", size=11))
    stats_text.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
    
    # Buttons
    button_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
    button_frame.pack(fill=ctk.X, padx=10, pady=5)
    
    def update_display():
        stats = dashboard_manager.get_stats()
        display_text = f"""📊 THỐNG KÊ TỔNG QUAN
{'='*25}
🎯 Tổng phát hiện: {stats['total_detections']}

📋 CHI TIẾT THEO LỚP:
"""
        if stats['class_counts']:
            for name, count in sorted(stats['class_counts'].items()):
                display_text += f"• {name}: {count}\n"
        else:
            display_text += "Chưa có dữ liệu\n"
        
        if stats['confidence_history']:
            recent = stats['confidence_history'][-3:]
            avg = sum(recent) / len(recent)
            display_text += f"\n📈 CONFIDENCE (3 gần nhất):\n"
            display_text += f"Trung bình: {avg:.3f}\n"
        
        display_text += f"\n🕒 {datetime.now().strftime('%H:%M:%S')}"
        
        stats_text.delete("1.0", "end")
        stats_text.insert("1.0", display_text)
    
    # Buttons
    ctk.CTkButton(button_frame, text="🔄 Refresh", command=update_display, width=80).pack(side=ctk.LEFT, padx=2)
    ctk.CTkButton(button_frame, text="🗑️ Reset", command=lambda: [dashboard_manager.reset_stats(), update_display()], width=80).pack(side=ctk.LEFT, padx=2)
    
    return stats_text, update_display
