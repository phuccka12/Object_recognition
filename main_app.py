# File: main_app.py (Phiên bản v5.2 - Tích hợp Đa luồng)
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import app_logic
import os
import threading # Import thư viện đa luồng

class ObjectDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trạm Phân Tích AI Đa Năng - v5.2 (Multi-threaded)")
        # ... (phần __init__ còn lại giữ nguyên như cũ)
        self.root.geometry("1100x700")
        self.is_processing_video = False
        self.image_path = None
        self.result_image = None
        self.main_frame = ctk.CTkFrame(root, corner_radius=0)
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        self.control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.control_frame.pack(fill=ctk.X, pady=5)
        self.model_selection_label = ctk.CTkLabel(self.control_frame, text="Chọn Model:")
        self.model_selection_label.pack(side=ctk.LEFT, padx=(10,0), pady=5)
        self.model_combobox = ctk.CTkComboBox(self.control_frame, values=list(app_logic.AVAILABLE_MODELS.keys()), command=self.on_model_select)
        self.model_combobox.set(list(app_logic.AVAILABLE_MODELS.keys())[0])
        self.model_combobox.pack(side=ctk.LEFT, padx=5, pady=5)
        self.btn_load_img = ctk.CTkButton(self.control_frame, text="Tải Ảnh", command=self.load_image)
        self.btn_load_img.pack(side=ctk.LEFT, padx=5, pady=5)
        self.btn_detect_img = ctk.CTkButton(self.control_frame, text="Nhận diện Ảnh", command=self.detect_objects_image)
        self.btn_detect_img.pack(side=ctk.LEFT, padx=5, pady=5)
        self.btn_load_vid = ctk.CTkButton(self.control_frame, text="Chọn Video", command=self.select_video)
        self.btn_load_vid.pack(side=ctk.LEFT, padx=5, pady=5)
        self.btn_webcam = ctk.CTkButton(self.control_frame, text="Mở Webcam", command=self.open_webcam)
        self.btn_webcam.pack(side=ctk.LEFT, padx=5, pady=5)
        self.btn_stop = ctk.CTkButton(self.control_frame, text="Dừng", command=self.stop_processing, state="disabled", fg_color="red", hover_color="#C21807")
        self.btn_stop.pack(side=ctk.RIGHT, padx=5, pady=5)
        self.btn_save = ctk.CTkButton(self.control_frame, text="Lưu Ảnh", command=self.save_image)
        self.btn_save.pack(side=ctk.RIGHT, padx=5, pady=5)
        self.display_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.display_frame.pack(fill=ctk.BOTH, expand=True)
        self.image_label = ctk.CTkLabel(self.display_frame, text="Sẵn sàng chiến đấu!", corner_radius=10)
        self.image_label.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 5))
        self.data_label = ctk.CTkLabel(self.display_frame, text="--- Báo cáo sẽ hiển thị ở đây ---", justify=ctk.LEFT, anchor="nw", corner_radius=10, fg_color=("gray85", "gray20"))
        self.data_label.pack(side=ctk.RIGHT, fill=ctk.BOTH, expand=False, padx=(5, 0))

    # --- CÁC HÀM CỐT LÕI ĐÃ ĐƯỢC NÂNG CẤP ---
    def start_video_processing(self, source):
        """Hàm trung tâm để bắt đầu xử lý video trong một luồng mới."""
        if self.is_processing_video:
            return # Tránh khởi động nhiều luồng cùng lúc
        
        self.data_label.configure(text="")
        self.set_processing_state(True)
        
        # Tạo và khởi động "Phụ tá AI" (luồng mới)
        self.video_thread = threading.Thread(
            target=app_logic.process_video_stream,
            args=(source, self.image_label, self.data_label, self)
        )
        self.video_thread.daemon = True # Cho phép chương trình chính thoát dù luồng phụ còn chạy
        self.video_thread.start()

    def select_video(self):
        """Hàm được gọi khi nhấn nút 'Chọn Video'."""
        file_path = filedialog.askopenfilename(title="Chọn một file video", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if file_path:
            self.start_video_processing(file_path)

    def open_webcam(self):
        """Hàm được gọi khi nhấn nút 'Mở Webcam'."""
        # Số 0 thường là webcam mặc định
        self.start_video_processing(0)

    # ... (các hàm khác giữ nguyên như cũ, không cần dán lại)
    def on_model_select(self, selected_model):
        if not app_logic.switch_model(selected_model):
             messagebox.showerror("Lỗi", f"Không thể tải model '{selected_model}'.\nHãy chắc chắn file 'models/best.pt' tồn tại.")
             self.model_combobox.set(list(app_logic.AVAILABLE_MODELS.keys())[0])
             app_logic.switch_model(self.model_combobox.get())
        else:
             messagebox.showinfo("Thành công", f"Đã chuyển sang model '{selected_model}'")
    def set_processing_state(self, is_processing):
        self.is_processing_video = is_processing
        state = "disabled" if is_processing else "normal"
        for btn in [self.btn_load_img, self.btn_detect_img, self.btn_load_vid, self.btn_webcam, self.btn_save]:
            btn.configure(state=state)
        self.model_combobox.configure(state=state)
        self.btn_stop.configure(state="normal" if is_processing else "disabled")
    def stop_processing(self):
        self.set_processing_state(False)
    def load_image(self):
        self.stop_processing()
        file_path = filedialog.askopenfilename(title="Chọn một file ảnh", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image_path = file_path
            original_img = Image.open(self.image_path)
            w, h = original_img.size
            display_w, display_h = 750, 600
            ratio = min(display_w/w, display_h/h)
            new_size = (int(w*ratio), int(h*ratio))
            ctk_img = ctk.CTkImage(light_image=original_img, dark_image=original_img, size=new_size)
            self.image_label.configure(text="", image=ctk_img)
            self.data_label.configure(text="--- Báo cáo sẽ hiển thị ở đây ---")
            self.result_image = None
    def detect_objects_image(self):
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng 'Tải Ảnh' trước!")
            return
        result_image, detected_info = app_logic.detect_objects_in_image(self.image_path)
        if result_image:
            self.result_image = result_image
            w, h = self.result_image.size
            display_w, display_h = 750, 600
            ratio = min(display_w/w, display_h/h)
            new_size = (int(w*ratio), int(h*ratio))
            ctk_img = ctk.CTkImage(light_image=self.result_image, dark_image=self.result_image, size=new_size)
            self.image_label.configure(image=ctk_img)
            self.data_label.configure(text=detected_info)
            messagebox.showinfo("Thành công", "Đã nhận diện ảnh xong!")
    def save_image(self):
        if not self.result_image:
            messagebox.showwarning("Cảnh báo", "Chỉ có thể lưu kết quả từ chức năng Nhận diện Ảnh.")
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")])
        if save_path:
            self.result_image.save(save_path)
            messagebox.showinfo("Thành công", f"Đã lưu tại: {save_path}")

# --- Khởi chạy Chiến dịch ---
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    if not os.path.exists('models'):
        os.makedirs('models')
        print("Đã tạo thư mục 'models'. Hãy đặt file best.pt của bạn vào đây.")
    root = ctk.CTk()
    app = ObjectDetectorApp(root)
    root.mainloop()