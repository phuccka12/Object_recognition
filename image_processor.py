# File: image_processor.py - Xử lý ảnh và ROI
import customtkinter as ctk
from PIL import Image, ImageEnhance, ImageFilter
import os
import threading
from tkinter import filedialog, messagebox

class ImageProcessor:
    def __init__(self):
        self.brightness = 1.0
        self.contrast = 1.0
        self.sharpness = 1.0
        self.filter_type = "Không"
        self.roi_coordinates = None
        self.roi_enabled = False
    
    def set_roi(self, x1, y1, x2, y2):
        """Thiết lập ROI"""
        self.roi_coordinates = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        self.roi_enabled = True
    
    def disable_roi(self):
        """Tắt ROI"""
        self.roi_enabled = False
    
    def process_image(self, image):
        """Xử lý ảnh với các settings hiện tại"""
        if not image:
            return None
        
        img = image.copy()
        
        # Apply enhancements
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(self.brightness)
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(self.contrast)
        
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(self.sharpness)
        
        # Apply filters
        if self.filter_type == "Blur":
            img = img.filter(ImageFilter.BLUR)
        elif self.filter_type == "Sharpen":
            img = img.filter(ImageFilter.SHARPEN)
        elif self.filter_type == "Edge Enhance":
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif self.filter_type == "Emboss":
            img = img.filter(ImageFilter.EMBOSS)
        elif self.filter_type == "Gaussian Blur":
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
        
        return img
    
    def batch_process_images(self, image_paths, output_folder, detect_func):
        """Xử lý batch nhiều ảnh"""
        results = []
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        for i, image_path in enumerate(image_paths):
            try:
                print(f"Processing {i+1}/{len(image_paths)}: {os.path.basename(image_path)}")
                
                # Load và process image
                original_img = Image.open(image_path)
                processed_img = self.process_image(original_img)
                
                # Save processed image temporarily
                temp_path = "temp_processed.jpg"
                processed_img.save(temp_path)
                
                # Detect objects
                result_image, detected_info = detect_func(temp_path)
                
                if result_image:
                    filename = os.path.splitext(os.path.basename(image_path))[0]
                    output_path = os.path.join(output_folder, f"{filename}_result.jpg")
                    result_image.save(output_path)
                    
                    report_path = os.path.join(output_folder, f"{filename}_report.txt")
                    with open(report_path, 'w', encoding='utf-8') as f:
                        f.write(detected_info)
                    
                    results.append({"input": image_path, "output": output_path, "status": "success"})
                else:
                    results.append({"input": image_path, "status": "failed", "error": detected_info})
                
                # Cleanup
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
            except Exception as e:
                results.append({"input": image_path, "status": "error", "error": str(e)})
        
        return results

def create_image_processing_frame(parent_frame, processor, apply_callback):
    """Tạo frame xử lý ảnh"""
    # Title
    title = ctk.CTkLabel(parent_frame, text="🎨 XỬ LÝ ẢNH", font=ctk.CTkFont(size=14, weight="bold"))
    title.pack(pady=5)
    
    # Controls frame
    controls = ctk.CTkFrame(parent_frame, fg_color="transparent")
    controls.pack(fill=ctk.X, padx=10, pady=5)
    
    # Brightness
    ctk.CTkLabel(controls, text="Sáng:", width=50).pack(side=ctk.LEFT, padx=2)
    brightness_slider = ctk.CTkSlider(controls, from_=0.5, to=2.0, width=80,
                                     command=lambda v: [setattr(processor, 'brightness', v), apply_callback()])
    brightness_slider.set(1.0)
    brightness_slider.pack(side=ctk.LEFT, padx=2)
    
    # Contrast
    ctk.CTkLabel(controls, text="Tương phản:", width=80).pack(side=ctk.LEFT, padx=2)
    contrast_slider = ctk.CTkSlider(controls, from_=0.5, to=2.0, width=80,
                                   command=lambda v: [setattr(processor, 'contrast', v), apply_callback()])
    contrast_slider.set(1.0)
    contrast_slider.pack(side=ctk.LEFT, padx=2)
    
    # Sharpness
    ctk.CTkLabel(controls, text="Sắc nét:", width=60).pack(side=ctk.LEFT, padx=2)
    sharpness_slider = ctk.CTkSlider(controls, from_=0.0, to=3.0, width=80,
                                    command=lambda v: [setattr(processor, 'sharpness', v), apply_callback()])
    sharpness_slider.set(1.0)
    sharpness_slider.pack(side=ctk.LEFT, padx=2)
    
    # Second row for filter and buttons
    controls2 = ctk.CTkFrame(parent_frame, fg_color="transparent")
    controls2.pack(fill=ctk.X, padx=10, pady=5)
    
    # Filter
    ctk.CTkLabel(controls2, text="Bộ lọc:").pack(side=ctk.LEFT, padx=2)
    filter_combo = ctk.CTkComboBox(controls2, values=["Không", "Blur", "Sharpen", "Edge Enhance", "Emboss", "Gaussian Blur"], 
                                  width=100, command=lambda v: [setattr(processor, 'filter_type', v), apply_callback()])
    filter_combo.set("Không")
    filter_combo.pack(side=ctk.LEFT, padx=5)
    
    # Reset button
    def reset():
        processor.brightness = 1.0
        processor.contrast = 1.0
        processor.sharpness = 1.0
        processor.filter_type = "Không"
        brightness_slider.set(1.0)
        contrast_slider.set(1.0)
        sharpness_slider.set(1.0)
        filter_combo.set("Không")
        apply_callback()
    
    ctk.CTkButton(controls2, text="🔄 Reset", command=reset, width=60).pack(side=ctk.LEFT, padx=5)
    
    return brightness_slider, contrast_slider, sharpness_slider, filter_combo
