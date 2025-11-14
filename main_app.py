# File: main_app.py (Phiên bản v6.1 - Modular & Clean)
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import app_logic
import os
import threading

# Import UI components
from ui_components import DashboardPanel, AdvancedFeaturesPanel
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
        values = list(app_logic.AVAILABLE_MODELS.keys())
        self.model_combobox = ctk.CTkComboBox(self.control_frame, values=values,
                                             command=self.on_model_select, width=150)
        # Chỉ set giá trị mặc định khi có model trong danh sách
        if values:
            try:
                self.model_combobox.set(values[0])
            except Exception:
                pass
        self.model_combobox.pack(side=ctk.LEFT, padx=5)

        # --- Model info area (hiển thị ngay khi load hoặc chọn model) ---
        # dùng tkinter.StringVar để đảm bảo tương thích
        import tkinter as _tk
        self.model_info_frame = ctk.CTkFrame(self.control_frame, fg_color="transparent")
        # nhỏ gọn: hiển thị path, số lớp, kích thước file
        self.model_info_path_var = _tk.StringVar(value="Path: N/A")
        self.model_info_classes_var = _tk.StringVar(value="Classes: N/A")
        self.model_info_size_var = _tk.StringVar(value="Size: N/A")

        ctk.CTkLabel(self.model_info_frame, textvariable=self.model_info_path_var, anchor="w").pack(side=ctk.LEFT, padx=(8,6))
        ctk.CTkLabel(self.model_info_frame, textvariable=self.model_info_classes_var, anchor="w").pack(side=ctk.LEFT, padx=(6,6))
        ctk.CTkLabel(self.model_info_frame, textvariable=self.model_info_size_var, anchor="w").pack(side=ctk.LEFT, padx=(6,10))
        self.model_info_frame.pack(side=ctk.LEFT, padx=5)

        # Load model button
        ctk.CTkButton(self.control_frame, text="📥 Load .pt", command=self.load_model_file_dialog, width=90).pack(side=ctk.LEFT, padx=2)

        # Management button (replaces confidence slider)
        ctk.CTkButton(self.control_frame, text="⚙️ Quản lý", command=self.open_manage_models, width=90).pack(side=ctk.LEFT, padx=5)

        # Main buttons
        self.create_main_buttons()
        
        # Stop button
        self.btn_stop = ctk.CTkButton(self.control_frame, text="⏹️ Stop", command=self.stop_processing, 
                                     state="disabled", fg_color="red", width=70)
        self.btn_stop.pack(side=ctk.RIGHT, padx=5)

        # Cập nhật model info ban đầu (nếu có model mặc định)
        try:
            sel = self.model_combobox.get()
            if sel:
                self.update_model_info(sel)
            else:
                # nếu không có selection, lấy thông tin tổng quan
                self.update_model_info(None)
        except Exception:
            pass

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
        # === VÙNG HIỂN THỊ ẢNH (MỞ RỘNG, CHO PHÉP EXPAND) ===
        # Tăng chiều cao mặc định và cho phép vùng ảnh mở rộng khi resize cửa sổ
        self.image_frame = ctk.CTkFrame(self.left_frame, height=650)
        # Cho phép frame mở rộng theo cả chiều ngang và dọc
        self.image_frame.pack(fill=ctk.BOTH, expand=True, pady=(0, 5))
        # Giữ pack_propagate để nội dung có thể điều chỉnh kích thước bên trong
        self.image_frame.pack_propagate(True)

        self.image_label = ctk.CTkLabel(
            self.image_frame,
            text="🎯 AI Object Detection Studio\n\n📸 Tải ảnh để bắt đầu phân tích",
            font=ctk.CTkFont(size=16),
            corner_radius=10
        )
        # Thêm padding nhỏ để ảnh hiển thị lớn và đẹp hơn
        self.image_label.pack(fill=ctk.BOTH, expand=True, padx=8, pady=8)
        
    # (Image processing UI removed)

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

    # Image processing feature removed — no per-image adjustments available in this build.

    def detect_objects_image(self):
        """Nhận diện đối tượng trong ảnh"""
        # Dừng video processing trước khi nhận diện ảnh
        if self.is_processing_video:
            self.stop_processing()
            
        if not self.image_path:
            messagebox.showwarning("Cảnh báo", "Vui lòng 'Tải Ảnh' trước!")
            return
        
        detect_image = self.processed_image if self.processed_image else self.original_image

        # Ensure we have a PIL Image. If detect_image is a numpy array (OpenCV), convert it.
        pil_img = None
        try:
            if hasattr(detect_image, 'convert') and isinstance(detect_image, Image.Image):
                pil_img = detect_image
            else:
                # assume numpy array (BGR) from OpenCV
                import numpy as _np
                if isinstance(detect_image, _np.ndarray):
                    # convert BGR to RGB
                    from PIL import Image as _PILImage
                    rgb = _PILImage.fromarray(detect_image[..., ::-1])
                    pil_img = rgb
                else:
                    # try to coerce via PIL
                    pil_img = Image.fromarray(detect_image)
        except Exception:
            # As a last resort, try to open from path if original was a path string
            if isinstance(detect_image, str) and os.path.exists(detect_image):
                pil_img = Image.open(detect_image)

        if pil_img is None:
            messagebox.showerror("Lỗi", "Không thể chuẩn hóa ảnh để nhận diện.")
            return

        # Choose file extension based on mode: use PNG if image has alpha channel
        if pil_img.mode == 'RGBA' or 'A' in pil_img.getbands():
            temp_path = "temp_processed.png"
            save_img = pil_img  # PNG supports alpha
        else:
            temp_path = "temp_processed.jpg"
            # Convert to RGB for JPEG
            if pil_img.mode != 'RGB':
                save_img = pil_img.convert('RGB')
            else:
                save_img = pil_img

        try:
            save_img.save(temp_path)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lưu tạm ảnh: {e}")
            return
        
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
        # Deprecated: confidence slider removed. This method kept for backward compatibility but does nothing.
        try:
            app_logic.set_confidence_threshold(float(value))
        except Exception:
            pass

    def open_manage_models(self):
        """Mở cửa sổ quản lý model: đặt active, unregister hoặc mở thư mục models/"""
        try:
            win = ctk.CTkToplevel(self.root)
        except Exception:
            # Fall back to tkinter Toplevel if CTkToplevel not available
            from tkinter import Toplevel
            win = Toplevel(self.root)

        win.title("Quản lý models")
        win.geometry("420x180")

        ctk.CTkLabel(win, text="Quản lý models đã đăng ký", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,5))

        values = list(app_logic.AVAILABLE_MODELS.keys())
        model_select = ctk.CTkComboBox(win, values=values, width=300)
        if values:
            try:
                model_select.set(values[0])
            except Exception:
                pass
        model_select.pack(pady=5)

        btn_frame = ctk.CTkFrame(win, fg_color="transparent")
        btn_frame.pack(pady=8)

        def set_active():
            sel = model_select.get()
            if not sel:
                messagebox.showwarning("Chọn model", "Vui lòng chọn model để đặt active")
                return
            if app_logic.switch_model(sel):
                # update main combobox
                values = list(app_logic.AVAILABLE_MODELS.keys())
                self.model_combobox.configure(values=values)
                try:
                    self.model_combobox.set(sel)
                    try:
                        self.update_model_info(sel)
                    except Exception:
                        pass
                except Exception:
                    pass
                messagebox.showinfo("Thành công", f"Đã chuyển sang model: {sel}")
            else:
                messagebox.showerror("Lỗi", f"Không thể tải model: {sel}")

        def unregister():
            sel = model_select.get()
            if not sel:
                messagebox.showwarning("Chọn model", "Vui lòng chọn model để unregister")
                return
            if sel in app_logic.AVAILABLE_MODELS:
                # Do not delete the model file, only unregister from the app
                del app_logic.AVAILABLE_MODELS[sel]
                # update both combo boxes
                values = list(app_logic.AVAILABLE_MODELS.keys())
                model_select.configure(values=values)
                self.model_combobox.configure(values=values)
                if values:
                    try:
                        model_select.set(values[0])
                        self.model_combobox.set(values[0])
                        # update model info to new selection
                        try:
                            self.update_model_info(values[0])
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:
                    # no models left
                    self.model_combobox.set("")
                    try:
                        self.update_model_info(None)
                    except Exception:
                        pass
                messagebox.showinfo("Đã bỏ đăng ký", f"Đã bỏ đăng ký model: {sel}")
            else:
                messagebox.showwarning("Không tồn tại", "Model không tồn tại trong danh sách")

        def open_models_folder():
            models_dir = os.path.join(os.getcwd(), 'models')
            if not os.path.exists(models_dir):
                os.makedirs(models_dir)
            try:
                os.startfile(models_dir)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể mở thư mục models: {e}")

        ctk.CTkButton(btn_frame, text="Đặt active", command=set_active, width=100).pack(side=ctk.LEFT, padx=6)
        ctk.CTkButton(btn_frame, text="Bỏ đăng ký", command=unregister, width=100).pack(side=ctk.LEFT, padx=6)
        ctk.CTkButton(btn_frame, text="Mở thư mục models", command=open_models_folder, width=140).pack(side=ctk.LEFT, padx=6)

        ctk.CTkButton(win, text="Đóng", command=win.destroy, width=80).pack(pady=(6,10))

    def show_model_info(self):
        """Hiển thị thông tin model"""
        # if combobox has selection, pass that key to get more accurate path/size
        sel = self.model_combobox.get() if hasattr(self, 'model_combobox') else None
        info = app_logic.get_model_info(sel if sel else None)
        info_text = f"""🤖 MODEL: {info['name']}
📊 Classes: {info['classes']}
⚙️ Confidence: {app_logic.current_confidence}"""
        messagebox.showinfo("Model Info", info_text)

    def update_model_info(self, model_key=None):
        """Cập nhật widget hiển thị model info dựa trên model_key (key trong AVAILABLE_MODELS) hoặc combobox hiện tại."""
        try:
            key = model_key if model_key else (self.model_combobox.get() if hasattr(self, 'model_combobox') else None)
            info = app_logic.get_model_info(key if key else None)
            path = info.get('path') or 'N/A'
            classes = info.get('classes') or 0
            size = info.get('file_size') or 'N/A'
            self.model_info_path_var.set(f"Path: {path}")
            self.model_info_classes_var.set(f"Classes: {classes}")
            self.model_info_size_var.set(f"Size: {size}")
        except Exception as e:
            print(f'Failed to update model info UI: {e}')

    def load_model_file_dialog(self):
        """Open file dialog to choose a local .pt model and load/register it."""
        file_path = filedialog.askopenfilename(title="Chọn model .pt", filetypes=[("PyTorch model", "*.pt")])
        if not file_path:
            return

        result = app_logic.load_model_file(file_path, register=True)
        if not result:
            messagebox.showerror("Lỗi", f"Không thể load model từ: {file_path}")
            return

        # result is the key name registered in AVAILABLE_MODELS
        # cập nhật combobox values
        values = list(app_logic.AVAILABLE_MODELS.keys())
        self.model_combobox.configure(values=values)
        try:
            self.model_combobox.set(result)
        except Exception:
            pass
        # Cập nhật model info ngay sau khi load
        try:
            self.update_model_info(result)
        except Exception:
            pass

        messagebox.showinfo("Thành công", f"Đã load và đăng ký model: {result}")

    def on_model_select(self, selected_model):
        """Chọn model"""
        if not app_logic.switch_model(selected_model):
            messagebox.showerror("Lỗi", f"Không thể tải model '{selected_model}'")
            self.model_combobox.set(list(app_logic.AVAILABLE_MODELS.keys())[0])
        else:
            messagebox.showinfo("Thành công", f"Đã chuyển sang model '{selected_model}'")
            # cập nhật thông tin model trên UI
            try:
                self.update_model_info(selected_model)
            except Exception:
                pass

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