# File: main_app.py (Phiên bản v6.1 - Modular & Clean)
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import app_logic
import os
import threading

# Import UI components
from ui_components import DashboardPanel, ImageProcessingPanel, AdvancedFeaturesPanel
from image_utils import ImageProcessor, BatchProcessor

class ObjectDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 AI Object Detection Studio v6.1")
        self.root.geometry("1200x800")
        
        # State variables
        self.is_processing_video = False
        self.image_path = None
        self.result_image = None
        self.original_image = None
        self.processed_image = None
        
        self.setup_ui()
        self.auto_update_dashboard()

    def setup_ui(self):
        """Thiết lập giao diện chính"""
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        self.setup_top_controls()
        self.setup_main_content()

    def setup_top_controls(self):
        """Thiết lập thanh điều khiển trên"""
        self.control_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.control_frame.pack(fill=ctk.X, pady=5)
        
        # Model selection
        ctk.CTkLabel(self.control_frame, text="Model:").pack(side=ctk.LEFT, padx=(10,5))
        self.model_combobox = ctk.CTkComboBox(self.control_frame, values=list(app_logic.AVAILABLE_MODELS.keys()), 
                                             command=self.on_model_select, width=150)
        self.model_combobox.set(list(app_logic.AVAILABLE_MODELS.keys())[0])
        self.model_combobox.pack(side=ctk.LEFT, padx=5)
        
        # Confidence
        ctk.CTkLabel(self.control_frame, text="Confidence:").pack(side=ctk.LEFT, padx=(10,5))
        self.conf_slider = ctk.CTkSlider(self.control_frame, from_=0.1, to=0.9, 
                                        command=self.update_confidence, width=100)
        self.conf_slider.set(0.5)
        self.conf_slider.pack(side=ctk.LEFT, padx=5)
        
        self.conf_label = ctk.CTkLabel(self.control_frame, text="0.5", width=30)
        self.conf_label.pack(side=ctk.LEFT, padx=5)
        
        # Main buttons
        self.create_main_buttons()
        
        # Stop button
        self.btn_stop = ctk.CTkButton(self.control_frame, text="⏹️ Stop", command=self.stop_processing, 
                                     state="disabled", fg_color="red", width=70)
        self.btn_stop.pack(side=ctk.RIGHT, padx=5)

    def create_main_buttons(self):
        """Tạo các nút chính"""
        buttons = [
            ("📁 Tải Ảnh", self.load_image),
            ("🎯 Nhận diện", self.detect_objects_image),
            ("🎬 Video", self.select_video),
            ("📹 Webcam", self.open_webcam),
            ("ℹ️ Info", self.show_model_info)
        ]
        
        for text, command in buttons:
            ctk.CTkButton(self.control_frame, text=text, command=command, width=90).pack(side=ctk.LEFT, padx=2)

    def setup_main_content(self):
        """Thiết lập nội dung chính"""
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill=ctk.BOTH, expand=True, pady=5)
        
        # Left: Image display + processing
        self.left_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.left_frame.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=(0, 5))
        
        self.setup_image_area()
        
        # Right: Dashboard + advanced controls
        self.right_frame = ctk.CTkFrame(self.content_frame, width=320, fg_color=("gray90", "gray25"))
        self.right_frame.pack(side=ctk.RIGHT, fill=ctk.Y, padx=(5, 0))
        self.right_frame.pack_propagate(False)
        
        self.setup_right_panel()

    def setup_image_area(self):
        """Thiết lập khu vực hiển thị ảnh"""
        # === VÙNG HIỂN THỊ ẢNH (CỐ ĐỊNH CHIỀU CAO) ===
        self.image_frame = ctk.CTkFrame(self.left_frame, height=450)
        self.image_frame.pack(fill=ctk.X, pady=(0, 5))
        self.image_frame.pack_propagate(False)  # QUAN TRỌNG: Không cho frame tự động resize
        
        self.image_label = ctk.CTkLabel(
            self.image_frame, 
            text="🎯 AI Object Detection Studio\n\n📸 Tải ảnh để bắt đầu phân tích", 
            font=ctk.CTkFont(size=16), 
            corner_radius=10
        )
        self.image_label.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)
        
        # === VÙNG XỬ LÝ ẢNH (LUÔN Ở DƯỚI - CỐ ĐỊNH) ===
        self.processing_frame = ctk.CTkFrame(self.left_frame, fg_color=("gray90", "gray25"), height=130)
        self.processing_frame.pack(fill=ctk.X, pady=5)
        self.processing_frame.pack_propagate(False)  # QUAN TRỌNG: Giữ chiều cao cố định
        
        self.image_processor = ImageProcessingPanel(self.processing_frame, self.apply_image_processing)

    def setup_right_panel(self):
        """Thiết lập panel bên phải"""
        # Dashboard
        self.dashboard = DashboardPanel(self.right_frame)
        
        # Advanced features
        advanced_frame = ctk.CTkFrame(self.right_frame)
        advanced_frame.pack(fill=ctk.X, padx=10, pady=10)
        
        self.advanced_features = AdvancedFeaturesPanel(advanced_frame, self)

    # === CORE FUNCTIONS ===
    def load_image(self):
        """Tải ảnh"""
        # Dừng video processing trước khi tải ảnh
        if self.is_processing_video:
            self.stop_processing()
            
        file_path = filedialog.askopenfilename(title="Chọn một file ảnh", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(self.image_path)
            self.processed_image = None
            self.result_image = None
            
            ImageProcessor.display_image(self.original_image, self.image_label)
            # Reset processing và áp dụng ngay
            self.image_processor.reset_processing()
            # Áp dụng xử lý ảnh ngay sau khi reset
            self.apply_image_processing()

    def apply_image_processing(self, value=None):
        """Áp dụng xử lý ảnh"""
        if not self.original_image:
            return
        
        # Kiểm tra xem image_processor đã được khởi tạo chưa
        if not hasattr(self, 'image_processor'):
            return
        
        try:
            self.processed_image = ImageProcessor.apply_processing(
                self.original_image,
                self.image_processor.brightness_slider.get(),
                self.image_processor.contrast_slider.get(),
                self.image_processor.sharpness_slider.get(),
                self.image_processor.filter_combo.get()
            )
            
            if self.processed_image:
                ImageProcessor.display_image(self.processed_image, self.image_label)
                print(f"Processed: Brightness={self.image_processor.brightness_slider.get():.1f}, Contrast={self.image_processor.contrast_slider.get():.1f}")
        except Exception as e:
            print(f"Lỗi apply_image_processing: {e}")

    def detect_objects_image(self):
        """Nhận diện đối tượng trong ảnh"""
        # Dừng video processing trước khi nhận diện ảnh
        if self.is_processing_video:
            self.stop_processing()
            
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng 'Tải Ảnh' trước!")
            return
        
        detect_image = self.processed_image if self.processed_image else self.original_image
        temp_path = "temp_processed.jpg"
        detect_image.save(temp_path)
        
        try:
            result_image, detected_info = app_logic.detect_objects_in_image(temp_path)
            
            if result_image:
                self.result_image = result_image
                ImageProcessor.display_image(self.result_image, self.image_label)
                messagebox.showinfo("✅ Thành công", "Đã nhận diện ảnh xong!")
            else:
                messagebox.showwarning("⚠️ Cảnh báo", detected_info)
                
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Có lỗi xảy ra: {str(e)}")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def select_video(self):
        """Chọn video"""
        # Dừng bất kỳ xử lý nào đang chạy
        if self.is_processing_video:
            self.stop_processing()
            
        file_path = filedialog.askopenfilename(title="Chọn một file video", filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
        if file_path:
            self.start_video_processing(file_path)

    def open_webcam(self):
        """Mở webcam"""
        # Dừng bất kỳ xử lý nào đang chạy
        if self.is_processing_video:
            self.stop_processing()
            # Đợi một chút để đảm bảo đã dừng hoàn toàn
            self.root.after(1000, lambda: self.start_video_processing(0))
        else:
            self.start_video_processing(0)

    def start_video_processing(self, source):
        """Bắt đầu xử lý video"""
        # Kiểm tra xem có đang xử lý video không
        if self.is_processing_video:
            print("Đang xử lý video, không thể bắt đầu video mới")
            return
        
        print(f"Bắt đầu xử lý video từ nguồn: {source}")
        self.set_processing_state(True)
        
        # Tạo luồng xử lý video mới
        self.video_thread = threading.Thread(
            target=app_logic.process_video_stream,
            args=(source, self.image_label, self.dashboard.stats_text, self)
        )
        self.video_thread.daemon = True
        self.video_thread.start()

    def stop_processing(self):
        """Dừng xử lý video thực sự"""
        print("Đang dừng xử lý video...")
        self.is_processing_video = False
        
        # KHÔNG gọi join() để tránh lỗi RuntimeError
        # Thread sẽ tự động kết thúc khi is_processing_video = False
        
        self.set_processing_state(False)
        print("Đã dừng xử lý video")

    def set_processing_state(self, is_processing):
        """Cập nhật trạng thái xử lý"""
        self.is_processing_video = is_processing
        state = "disabled" if is_processing else "normal"
        
        # Disable/enable tất cả các nút chính
        buttons_to_control = [
            self.model_combobox,
            # Tìm và disable các nút chính
        ]
        
        # Disable tất cả buttons trong control_frame khi đang xử lý video
        for widget in self.control_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget != self.btn_stop:
                widget.configure(state=state)
            elif isinstance(widget, ctk.CTkComboBox):
                widget.configure(state=state)
        
        self.btn_stop.configure(state="normal" if is_processing else "disabled")
        
        # Reset hiển thị khi dừng
        if not is_processing:
            self.image_label.configure(
                text="🎯 AI Object Detection Studio\n\n📸 Tải ảnh để bắt đầu phân tích",
                image=""
            )

    def run_batch_processing(self, files, folder):
        """Chạy batch processing"""
        messagebox.showinfo("🔄 Processing", f"Đang xử lý {len(files)} files...")
        BatchProcessor.process_images(files, folder)

    # === EVENT HANDLERS ===
    def update_confidence(self, value):
        """Cập nhật confidence"""
        self.conf_label.configure(text=f"{value:.1f}")
        app_logic.set_confidence_threshold(value)

    def show_model_info(self):
        """Hiển thị thông tin model"""
        info = app_logic.get_model_info()
        info_text = f"""🤖 MODEL: {info['name']}
📊 Classes: {info['classes']}
⚙️ Confidence: {app_logic.current_confidence}"""
        messagebox.showinfo("Model Info", info_text)

    def on_model_select(self, selected_model):
        """Chọn model"""
        if not app_logic.switch_model(selected_model):
            messagebox.showerror("Lỗi", f"Không thể tải model '{selected_model}'")
            self.model_combobox.set(list(app_logic.AVAILABLE_MODELS.keys())[0])
        else:
            messagebox.showinfo("Thành công", f"Đã chuyển sang model '{selected_model}'")

    def auto_update_dashboard(self):
        """Tự động cập nhật dashboard"""
        if hasattr(self, 'dashboard'):
            self.dashboard.update_dashboard()
        self.root.after(5000, self.auto_update_dashboard)

# === KHỞI CHẠY ỨNG DỤNG ===
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    if not os.path.exists('models'):
        os.makedirs('models')
        print("Đã tạo thư mục 'models'. Hãy đặt file best.pt của bạn vào đây.")
    
    root = ctk.CTk()
    app = ObjectDetectorApp(root)
    root.mainloop()