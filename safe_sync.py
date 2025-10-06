#!/usr/bin/env python3
"""
Safe Git Sync - Backup, Pull, Resolve conflicts, Push
Usage: python safe_sync.py
"""

import subprocess
import shutil
import os
from datetime import datetime

def run_cmd(cmd):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_backup():
    """Tạo backup trước khi pull"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    
    print(f"📦 Creating backup: {backup_dir}")
    
    try:
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup main files
        files_to_backup = ['*.py', '*.md', '*.txt', '*.bat']
        for pattern in files_to_backup:
            success, stdout, stderr = run_cmd(f'copy {pattern} {backup_dir}\\ 2>nul')
        
        print(f"✅ Backup created successfully!")
        return backup_dir
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return None

def safe_git_sync():
    """Safe git sync with backup and conflict resolution"""
    print("🚀 Safe Git Sync - AI Object Detection Studio")
    print("=" * 50)
    
    # 1. Create backup
    backup_dir = create_backup()
    if not backup_dir:
        print("❌ Cannot proceed without backup!")
        return
    
    # 2. Check git status
    print("\n📋 Checking git status...")
    success, stdout, stderr = run_cmd("git status --porcelain")
    
    if stdout.strip():
        print("📝 You have uncommitted changes:")
        print(stdout)
        
        # Commit changes first
        commit_msg = input("Enter commit message (or press Enter to skip): ").strip()
        if commit_msg:
            print("💾 Committing your changes...")
            run_cmd("git add .")
            run_cmd(f'git commit -m "{commit_msg}"')
    
    # 3. Pull from remote
    print("\n⬇️  Pulling from GitHub...")
    success, stdout, stderr = run_cmd("git pull origin main")
    
    if not success:
        if "CONFLICT" in stderr or "conflict" in stderr:
            print("⚠️  MERGE CONFLICTS DETECTED!")
            print("🔧 Please resolve conflicts manually:")
            print("1. Edit conflicted files (look for <<<<<<< markers)")
            print("2. Run: git add .")
            print("3. Run: git commit -m 'Resolve merge conflicts'")
            print("4. Run: git push origin main")
            print(f"\n💾 Your original files are backed up in: {backup_dir}")
            return
        else:
            print(f"❌ Pull failed: {stderr}")
            return
    
    print("✅ Pull successful!")
    
    # 4. Push to remote
    print("\n⬆️  Pushing to GitHub...")
    success, stdout, stderr = run_cmd("git push origin main")
    
    if success:
        print("✅ Push successful!")
        print("🌐 Your code is now synced with GitHub!")
        
        # Clean up backup if everything went well
        response = input(f"\nDelete backup folder {backup_dir}? (y/N): ")
        if response.lower() == 'y':
            shutil.rmtree(backup_dir)
            print("🗑️  Backup cleaned up")
    else:
        print(f"❌ Push failed: {stderr}")
        print(f"💾 Your files are backed up in: {backup_dir}")

if __name__ == "__main__":
    safe_git_sync()
