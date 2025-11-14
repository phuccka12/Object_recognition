# File: ui_components.py - Các components UI
import customtkinter as ctk
from tkinter import filedialog, messagebox
from datetime import datetime
import app_logic

class DashboardPanel:
    def __init__(self, parent_frame):
        self.parent = parent_frame
        self.setup_dashboard()
    
    def setup_dashboard(self):
        """Thiết lập dashboard"""
        title = ctk.CTkLabel(self.parent, text="📊 DASHBOARD", font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)
        
        # Stats display
        stats_frame = ctk.CTkFrame(self.parent, height=200)
        stats_frame.pack(fill=ctk.X, padx=10, pady=5)
        stats_frame.pack_propagate(False)
        
        self.stats_text = ctk.CTkTextbox(stats_frame, height=180, font=ctk.CTkFont(family="Consolas", size=11))
        self.stats_text.pack(fill=ctk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        button_frame.pack(fill=ctk.X, padx=10, pady=5)
        
        ctk.CTkButton(button_frame, text="🔄 Refresh", command=self.update_dashboard, width=80).pack(side=ctk.LEFT, padx=2)
        ctk.CTkButton(button_frame, text="🗑️ Reset", command=self.reset_stats, width=80).pack(side=ctk.LEFT, padx=2)
    
    def update_dashboard(self):
        """Cập nhật dashboard"""
        try:
            stats = app_logic.get_detection_stats()
            
            dashboard_text = f"""📊 THỐNG KÊ TỔNG QUAN
{'='*25}
🎯 Tổng phát hiện: {stats['total_detections']}

📋 CHI TIẾT THEO LỚP:
"""
            
            if stats['class_counts']:
                for class_name, count in sorted(stats['class_counts'].items()):
                    dashboard_text += f"• {class_name}: {count}\n"
            else:
                dashboard_text += "Chưa có dữ liệu\n"
            
            if stats['confidence_history']:
                recent_conf = stats['confidence_history'][-3:]
                avg_conf = sum(recent_conf) / len(recent_conf)
                dashboard_text += f"\n📈 CONFIDENCE (3 gần nhất):\n"
                dashboard_text += f"Trung bình: {avg_conf:.3f}\n"
            
            dashboard_text += f"\n🕒 {datetime.now().strftime('%H:%M:%S')}"
            
            self.stats_text.delete("1.0", "end")
            self.stats_text.insert("1.0", dashboard_text)
            
        except Exception as e:
            print(f"Lỗi cập nhật dashboard: {e}")
    
    def reset_stats(self):
        """Reset thống kê"""
        app_logic.reset_stats()
        self.update_dashboard()
        messagebox.showinfo("🔄 Reset", "Đã reset thống kê")

# Image processing UI removed — per-image adjustment controls were removed from the application.

class AdvancedFeaturesPanel:
    def __init__(self, parent_frame, app_instance):
        self.parent = parent_frame
        self.app = app_instance
        self.setup_advanced()
    
    def setup_advanced(self):
        """Thiết lập tính năng nâng cao"""
        ctk.CTkLabel(self.parent, text="⚙️ TÍNH NĂNG NÂNG CAO", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=5)
        
        # Export buttons
        export_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        export_frame.pack(fill=ctk.X, pady=5)
        
        ctk.CTkButton(export_frame, text="📊 Export CSV", command=self.export_csv, width=100).pack(side=ctk.LEFT, padx=2)
        ctk.CTkButton(export_frame, text="📋 Export JSON", command=self.export_json, width=100).pack(side=ctk.LEFT, padx=2)
        
        # Batch processing
        ctk.CTkButton(self.parent, text="🔄 Xử lý hàng loạt", command=self.batch_process, width=200).pack(pady=5)
    
    def export_csv(self):
        """Xuất CSV"""
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename and app_logic.export_stats_to_csv(filename):
            messagebox.showinfo("✅ Success", f"Exported to: {filename}")
    
    def export_json(self):
        """Xuất JSON"""
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename and app_logic.export_stats_to_json(filename):
            messagebox.showinfo("✅ Success", f"Exported to: {filename}")
    
    def batch_process(self):
        """Xử lý hàng loạt"""
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg;*.png;*.jpeg;*.bmp")])
        if files:
            folder = filedialog.askdirectory()
            if folder:
                self.app.run_batch_processing(files, folder)
        files = filedialog.askopenfilenames(filetypes=[("Images", "*.jpg;*.png;*.jpeg;*.bmp")])
        if files:
            folder = filedialog.askdirectory()
            if folder:
                self.app.run_batch_processing(files, folder)






                