# Setup script for AI Object Detection Studio
# Chạy: python setup.py để cài đặt tự động

import subprocess
import sys
import os

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("🚀 Đang cài đặt AI Object Detection Studio...")
    print("=" * 50)
    
    try:
        # Upgrade pip trước
        print("📦 Updating pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Cài đặt requirements
        print("📚 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Tạo thư mục models nếu chưa có
        if not os.path.exists('models'):
            os.makedirs('models')
            print("📁 Created 'models' directory")
        
        print("=" * 50)
        print("✅ Cài đặt thành công!")
        print("🎯 Chạy ứng dụng: python main_app.py")
        print("💡 Đặt file model custom vào thư mục 'models/best.pt'")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi cài đặt: {e}")
        print("💡 Thử chạy: pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")

if __name__ == "__main__":
    install_requirements()
