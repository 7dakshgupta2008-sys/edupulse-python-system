# setup.py - 1-Click Setup & Migration Script for New Laptops
import subprocess
import sys
import os

def run_setup():
    print("=" * 60)
    print("🚀 STUDENT ACADEMIC MANAGEMENT SYSTEM — LAPTOP SETUP")
    print("=" * 60)

    # 1. Install required packages
    print("\n📦 Checking and installing Python dependencies (Flask, PyMySQL)...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "pymysql"], check=True)
        print("✅ Dependencies verified!")
    except Exception as e:
        print(f"⚠️ Dependency installation warning: {e}")

    # 2. Seed XAMPP MySQL Database if running
    print("\n🛢️ Checking XAMPP MySQL server...")
    try:
        from seed_mysql import seed_xampp_mysql
        success = seed_xampp_mysql()
        if success:
            print("✅ XAMPP MySQL database 'student_db' synced and ready!")
        else:
            print("ℹ️ XAMPP MySQL not active. Application will use database.json.")
    except Exception as e:
        print(f"ℹ️ XAMPP MySQL check info: {e}")

    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE!")
    print("To start the app on this laptop, run:")
    print("   python app.py")
    print("Then open browser to: http://localhost:5000/login")
    print("=" * 60)

if __name__ == '__main__':
    run_setup()
