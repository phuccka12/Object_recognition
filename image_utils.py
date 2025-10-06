# File: image_utils.py - Utilities cho xử lý ảnh
from PIL import Image, ImageEnhance, ImageFilter
import customtkinter as ctk
import os
import threading
import app_logic
from tkinter import messagebox

class ImageProcessor:
    @staticmethod
    def apply_processing(original_image, brightness, contrast, sharpness, filter_type):
        """Áp dụng xử lý ảnh"""
        if not original_image:
            return None
        
        try:
            img = original_image.copy()
            
            # Apply brightness
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)
            
            # Apply contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
            
            # Apply sharpness
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(sharpness)
            
            # Apply filter
            if filter_type == "Blur":
                img = img.filter(ImageFilter.BLUR)
            elif filter_type == "Sharpen":
                img = img.filter(ImageFilter.SHARPEN)
            elif filter_type == "Edge Enhance":
                img = img.filter(ImageFilter.EDGE_ENHANCE)
            elif filter_type == "Emboss":
                img = img.filter(ImageFilter.EMBOSS)
            
            return img
            
        except Exception as e:
            print(f"Lỗi xử lý ảnh: {e}")
            return None
    
    @staticmethod
    def display_image(image, label_widget, max_width=750, max_height=600):
        """Hiển thị ảnh lên label"""
        if not image:
            return
        
        try:
            w, h = image.size
            ratio = min(max_width/w, max_height/h)
            new_size = (int(w*ratio), int(h*ratio))
            ctk_img = ctk.CTkImage(light_image=image, dark_image=image, size=new_size)
            # XÓA TEXT CŨ khi hiển thị ảnh mới
            label_widget.configure(text="", image=ctk_img)
        except Exception as e:
            print(f"Lỗi hiển thị ảnh: {e}")

class BatchProcessor:
    @staticmethod
    def process_images(file_paths, output_folder):
        """Xử lý batch nhiều ảnh"""
        def run_batch():
            success_count = 0
            for i, file_path in enumerate(file_paths):
                try:
                    result_image, detected_info = app_logic.detect_objects_in_image(file_path)
                    if result_image:
                        filename = os.path.splitext(os.path.basename(file_path))[0]
                        output_path = os.path.join(output_folder, f"{filename}_detected.jpg")
                        result_image.save(output_path)
                        success_count += 1
                        print(f"Processed {i+1}/{len(file_paths)}: {filename}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
            
            messagebox.showinfo("✅ Completed", f"Processed {len(file_paths)} files\nSuccess: {success_count}")
        
        threading.Thread(target=run_batch, daemon=True).start()
