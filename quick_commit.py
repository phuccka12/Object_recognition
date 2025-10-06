#!/usr/bin/env python3
"""
Quick commit and push script for AI Object Detection Studio
Usage: python quick_commit.py "Your commit message"
"""

import subprocess
import sys
from datetime import datetime

def run_command(cmd, check=True):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return None

def auto_deploy():
    """Auto deploy to GitHub with conflict resolution"""
    print("🚀 AI Object Detection Studio - Auto Deploy")
    print("=" * 50)
    
    # Get commit message
    if len(sys.argv) > 1:
        commit_msg = " ".join(sys.argv[1:])
    else:
        commit_msg = f"Update project - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    print(f"📝 Commit message: {commit_msg}")
    
    # Check status
    print("\n[1/5] Checking git status...")
    status = run_command("git status --porcelain")
    if not status:
        print("✅ No changes to commit")
        return
    
    # Add files
    print("\n[2/5] Adding files...")
    run_command("git add .")
    
    # Commit
    print("\n[3/5] Committing...")
    run_command(f'git commit -m "{commit_msg}"')
    
    # Pull first
    print("\n[4/5] Pulling latest changes...")
    pull_result = run_command("git pull origin main", check=False)
    
    if pull_result is None:
        print("⚠️  Pull conflicts detected!")
        print("Please resolve conflicts manually:")
        print("1. Edit conflicted files")
        print("2. Run: git add .")
        print("3. Run: git commit -m 'Resolve conflicts'")
        print("4. Run: git push origin main")
        return
    
    # Push
    print("\n[5/5] Pushing to GitHub...")
    push_result = run_command("git push origin main", check=False)
    
    if push_result is None:
        print("⚠️  Push failed! Trying force push...")
        response = input("Force push (will overwrite remote)? (y/N): ")
        if response.lower() == 'y':
            run_command("git push origin main --force")
            print("✅ Force push completed!")
        else:
            print("❌ Push cancelled")
    else:
        print("✅ Successfully pushed to GitHub!")
        print("🌐 Repository updated at: https://github.com/phuccka12/Object_recognition")

if __name__ == "__main__":
    auto_deploy()
