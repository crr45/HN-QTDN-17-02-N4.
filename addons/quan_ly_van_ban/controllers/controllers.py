# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class ChatbotController(http.Controller):

    @http.route('/chatbot/message', type='json', auth='user')
    def chatbot_message(self, message, **kw):
        env = request.env
        
        # 1. Get Gemini API Key from System Parameters
        api_key = env['ir.config_parameter'].sudo().get_param('gemini_api_key')
        if not api_key:
            return {
                'status': 'error',
                'reply': 'Chào bạn! Hệ thống AI chưa được cấu hình API Key. Vui lòng truy cập "Cấu hình AI" trong menu QLVB để thiết lập Gemini API Key.'
            }
            
        # 2. Gather System Context
        try:
            # Customers (Khách hàng)
            customers = env['khach_hang'].sudo().search([], limit=20)
            cust_list = []
            for c in customers:
                status_label = dict(c._fields['trang_thai'].selection).get(c.trang_thai, c.trang_thai) if 'trang_thai' in c._fields else c.trang_thai
                cust_list.append(f"- {c.ma_khach_hang}: {c.ten_khach_hang} (SĐT: {c.so_dien_thoai or 'N/A'}, Email: {c.email or 'N/A'}, Trạng thái: {status_label})")
            cust_context = "\n".join(cust_list) if cust_list else "Chưa có khách hàng."
            
            # Employees (Nhân viên)
            employees = env['nhan_vien'].sudo().search([], limit=20)
            emp_list = []
            for e in employees:
                emp_list.append(f"- {e.ma_dinh_danh}: {e.ho_va_ten} (Email: {e.email or 'N/A'}, SĐT: {e.so_dien_thoai or 'N/A'})")
            emp_context = "\n".join(emp_list) if emp_list else "Chưa có nhân viên."
            
            # Inbound Documents (Văn bản đến)
            docs_den = env['van_ban_den'].sudo().search([], limit=15)
            den_list = []
            for d in docs_den:
                emp_name = d.nhan_vien_xu_ly_id.ho_va_ten if d.nhan_vien_xu_ly_id else 'N/A'
                den_list.append(f"- Số đến: {d.so_van_ban_den}, Ký hiệu: {d.so_hieu_van_ban}, Tên: {d.ten_van_ban} (Người xử lý: {emp_name})")
            den_context = "\n".join(den_list) if den_list else "Chưa có văn bản đến."
            
            # Outbound Documents (Văn bản đi)
            docs_di = env['van_ban_di'].sudo().search([], limit=15)
            di_list = []
            for d in docs_di:
                emp_name = d.nguoi_ky_id.ho_va_ten if d.nguoi_ky_id else 'N/A'
                di_list.append(f"- Số đi: {d.so_van_ban_di}, Ký hiệu: {d.so_hieu_van_ban}, Tên: {d.ten_van_ban} (Người ký: {emp_name})")
            di_context = "\n".join(di_list) if di_list else "Chưa có văn bản đi."
            
        except Exception as ex:
            _logger.exception("Lỗi lấy dữ liệu hệ thống làm ngữ cảnh chatbot")
            cust_context = "Không thể tải danh sách khách hàng."
            emp_context = "Không thể tải danh sách nhân viên."
            den_context = "Không thể tải danh sách văn bản đến."
            di_context = "Không thể tải danh sách văn bản đi."

        # 3. Build AI Prompt with system data
        prompt = f"""
Bạn là Trợ lý AI chuyên nghiệp tích hợp trực tiếp trong hệ thống quản trị nội bộ Odoo của FIT-DNU.
Dưới đây là thông tin dữ liệu thời gian thực từ hệ thống để bạn trả lời câu hỏi của người dùng:

--- CƠ SỞ DỮ LIỆU KHÁCH HÀNG ---
{cust_context}

--- CƠ SỞ DỮ LIỆU NHÂN VIÊN ---
{emp_context}

--- DANH SÁCH VĂN BẢN ĐẾN ---
{den_context}

--- DANH SÁCH VĂN BẢN ĐI ---
{di_context}

--- HƯỚNG DẪN TRẢ LỜI ---
1. Trả lời bằng tiếng Việt, thân thiện, chuyên nghiệp, ngắn gọn và tập trung trực tiếp vào câu hỏi.
2. Dùng dữ liệu hệ thống ở trên để trả lời chính xác thông tin khi được hỏi (như liệt kê, tra cứu trạng thái, người phụ trách, số hiệu văn bản).
3. Nếu người dùng hỏi thông tin không có trong danh sách trên, hãy thông báo lịch sự rằng không tìm thấy thông tin đó trong hệ thống và gợi ý họ kiểm tra lại.
4. Tránh bịa đặt thông tin không có trong ngữ cảnh được cung cấp.

Yêu cầu/Câu hỏi của người dùng: "{message}"
Trợ lý AI trả lời:
"""

        # 4. Invoke Gemini API
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                res_data = response.json()
                reply_text = res_data['candidates'][0]['content']['parts'][0]['text'].strip()
                return {
                    'status': 'success',
                    'reply': reply_text
                }
            else:
                _logger.error(f"Gemini API returned error: {response.text}")
                return {
                    'status': 'error',
                    'reply': f"Không thể lấy câu trả lời từ AI. Gemini API phản hồi lỗi (Mã lỗi: {response.status_code})."
                }
        except Exception as e:
            _logger.exception("Lỗi gọi Gemini API trong ChatbotController")
            return {
                'status': 'error',
                'reply': f"Đã xảy ra sự cố khi xử lý yêu cầu của bạn: {str(e)}"
            }
