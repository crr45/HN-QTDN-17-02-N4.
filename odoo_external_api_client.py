#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xmlrpc.client
import sys

def test_odoo_connection(url, db, username, password):
    print("=" * 60)
    print("BẮT ĐẦU KẾT NỐI ODOO EXTERNAL API")
    print(f"Địa chỉ: {url}")
    print(f"Cơ sở dữ liệu: {db}")
    print(f"Tài khoản: {username}")
    print("=" * 60)

    try:
        # 1. Kết nối và lấy thông tin phiên bản
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        version_info = common.version()
        print("[+] Kết nối thành công!")
        print(f"[+] Thông tin phiên bản Odoo: {version_info}")
    except Exception as e:
        print(f"[-] Thất bại khi kết nối tới {url}: {e}")
        print("[-] Hãy chắc chắn rằng Odoo đang hoạt động.")
        return False

    try:
        # 2. Xác thực thông tin đăng nhập
        uid = common.authenticate(db, username, password, {})
        if not uid:
            print("[-] Đăng nhập thất bại. Vui lòng kiểm tra lại thông tin cơ sở dữ liệu, tài khoản và mật khẩu.")
            return False
        print(f"[+] Xác thực thành công! ID Người dùng (UID): {uid}")
    except Exception as e:
        print(f"[-] Thất bại khi xác thực: {e}")
        return False

    # 3. Kết nối với phân hệ quản trị đối tượng (models)
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # --- DEMO TRUY XUẤT DỮ LIỆU ---
    try:
        print("\n--- 1. Kiểm tra mô hình nhân sự ('nhan_vien') ---")
        # Tìm danh sách ID nhân viên
        employee_ids = models.execute_kw(db, uid, password, 'nhan_vien', 'search', [[]])
        print(f"[+] Tìm thấy {len(employee_ids)} nhân viên trong hệ thống.")

        if employee_ids:
            # Đọc thông tin chi tiết nhân viên
            employees = models.execute_kw(db, uid, password, 'nhan_vien', 'read', [employee_ids], {'fields': ['ho_va_ten', 'ma_dinh_danh', 'email', 'tuoi']})
            print("[+] Danh sách nhân viên hiện tại:")
            for idx, emp in enumerate(employees, 1):
                print(f"  {idx}. {emp.get('ho_va_ten')} - Mã: {emp.get('ma_dinh_danh')} - Email: {emp.get('email')} - Tuổi: {emp.get('tuoi')}")
        else:
            # Tạo mới một nhân viên mẫu nếu danh sách trống
            print("[*] Không có nhân viên nào. Đang tạo nhân viên thử nghiệm...")
            new_emp_id = models.execute_kw(db, uid, password, 'nhan_vien', 'create', [{
                'ho_ten_dem': 'Nguyễn Văn',
                'ten': 'A',
                'que_quan': 'Hà Nội',
                'email': 'nguyenvana@gmail.com',
                'ngay_sinh': '1995-01-01'
            }])
            print(f"[+] Đã tạo mới nhân viên với ID: {new_emp_id}")

        print("\n--- 2. Kiểm tra mô hình loại văn bản ('loai_van_ban') ---")
        category_ids = models.execute_kw(db, uid, password, 'loai_van_ban', 'search', [[]])
        if category_ids:
            categories = models.execute_kw(db, uid, password, 'loai_van_ban', 'read', [category_ids], {'fields': ['ma_loai_van_ban', 'ten_loai_van_ban']})
            print("[+] Danh sách loại văn bản:")
            for cat in categories:
                print(f"  - [{cat.get('ma_loai_van_ban')}] {cat.get('ten_loai_van_ban')}")
        else:
            print("[*] Danh sách loại văn bản trống. Tạo loại văn bản mặc định...")
            cat_id = models.execute_kw(db, uid, password, 'loai_van_ban', 'create', [{
                'ma_loai_van_ban': 'QD',
                'ten_loai_van_ban': 'Quyết định'
            }])
            print(f"[+] Đã tạo loại văn bản mới, ID: {cat_id}")

        print("\n--- 3. Kiểm tra mô hình văn bản đến ('van_ban_den') ---")
        doc_ids = models.execute_kw(db, uid, password, 'van_ban_den', 'search', [[]])
        print(f"[+] Tìm thấy {len(doc_ids)} văn bản đến.")
        if doc_ids:
            docs = models.execute_kw(db, uid, password, 'van_ban_den', 'read', [doc_ids], {'fields': ['ten_van_ban', 'so_van_ban_den', 'so_hieu_van_ban']})
            for doc in docs:
                print(f"  - {doc.get('ten_van_ban')} (Số đến: {doc.get('so_van_ban_den')}, Ký hiệu: {doc.get('so_hieu_van_ban')})")

    except Exception as e:
        print(f"[-] Đã xảy ra lỗi khi thực hiện thao tác cơ sở dữ liệu: {e}")
        return False

    print("\n" + "=" * 60)
    print("HOÀN THÀNH KIỂM TRA EXTERNAL API!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    url = "http://localhost:8069"
    db = "nhom4"
    username = "admin"
    password = "admin"

    if len(sys.argv) > 1:
        # Nếu truyền tham số từ dòng lệnh
        # Định dạng: python odoo_external_api_client.py <url> <db> <username> <password>
        url = sys.argv[1] if len(sys.argv) > 1 else url
        db = sys.argv[2] if len(sys.argv) > 2 else db
        username = sys.argv[3] if len(sys.argv) > 3 else username
        password = sys.argv[4] if len(sys.argv) > 4 else password

    test_odoo_connection(url, db, username, password)
