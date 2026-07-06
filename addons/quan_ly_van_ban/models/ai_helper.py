# -*- coding: utf-8 -*-
import requests
import json
import logging

_logger = logging.getLogger(__name__)

def analyze_document_text(env, title, content):
    """
    Hàm phân tích văn bản sử dụng Gemini API hoặc Mock fallback
    """
    if not title:
        title = ""
    if not content:
        content = ""

    # 1. Lấy tất cả loại văn bản có sẵn trong DB
    categories = env['loai_van_ban'].search([])
    categories_list = [cat.ten_loai_van_ban for cat in categories]

    # 2. Lấy tất cả nhân viên có sẵn trong DB
    employees = env['nhan_vien'].search([])
    employees_list = [emp.ho_va_ten for emp in employees]

    # 3. Lấy API Key từ ir.config_parameter
    api_key = env['ir.config_parameter'].sudo().get_param('gemini_api_key')

    if api_key:
        _logger.info("Đang gọi Google Gemini API để phân tích văn bản...")
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            headers = {'Content-Type': 'application/json'}
            
            prompt = f"""
Bạn là một trợ lý AI chuyên nghiệp phân loại và tóm tắt văn bản hành chính doanh nghiệp.
Nhiệm vụ của bạn là phân tích văn bản sau:
- Tiêu đề: {title}
- Nội dung: {content}

Dưới đây là danh sách các Loại văn bản có sẵn trong hệ thống (Tên loại văn bản):
{", ".join(categories_list)}

Dưới đây là danh sách các Nhân viên có sẵn trong hệ thống (Họ và tên):
{", ".join(employees_list)}

Vui lòng thực hiện:
1. Đề xuất Loại văn bản phù hợp nhất từ danh sách trên (trả về đúng Tên loại văn bản). Nếu không trùng khớp hoặc không chắc chắn, hãy trả về rỗng.
2. Đề xuất Nhân viên phù hợp nhất để xử lý/ký duyệt từ danh sách trên (trả về đúng Họ và tên). Nếu không trùng khớp, hãy trả về rỗng.
3. Viết một đoạn tóm tắt ngắn gọn (dưới 100 từ) bằng tiếng Việt làm nổi bật nội dung chính của văn bản này.

Bạn BẮT BUỘC phải trả về kết quả dưới định dạng JSON mẫu sau đây (không được kèm các ký tự định dạng markdown như ```json):
{{
  "category": "Tên loại văn bản phù hợp",
  "employee": "Họ và tên nhân viên phù hợp",
  "summary": "Nội dung tóm tắt tiếng Việt"
}}
"""
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "responseMimeType": "application/json"
                }
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=12)
            if response.status_code == 200:
                res_data = response.json()
                text_response = res_data['candidates'][0]['content']['parts'][0]['text']
                # Parse JSON trả về từ AI
                parsed_res = json.loads(text_response.strip())
                _logger.info(f"Gemini API phản hồi: {parsed_res}")
                return parsed_res, "success"
            else:
                _logger.error(f"Gemini API trả về lỗi: {response.text}")
        except Exception as e:
            _logger.exception(f"Lỗi khi gọi Gemini API: {e}")

    # Fallback / Mock Engine
    _logger.info("Sử dụng mô hình phân tích mô phỏng (Mock Rule-based Fallback)...")
    
    suggested_category = ""
    suggested_employee = ""
    
    title_lower = title.lower()
    content_lower = content.lower()
    combined_text = f"{title_lower} {content_lower}"
    
    # Mô phỏng phân loại dựa trên từ khóa
    for cat in categories:
        cat_name_lower = cat.ten_loai_van_ban.lower()
        if cat_name_lower in combined_text:
            suggested_category = cat.ten_loai_van_ban
            break
            
    if not suggested_category:
        if "quyết định" in combined_text or "qd" in combined_text:
            # Tìm danh mục Quyết định
            qd_cats = [c for c in categories_list if "quyết định" in c.lower()]
            if qd_cats:
                suggested_category = qd_cats[0]
        elif "hợp đồng" in combined_text or "hd" in combined_text:
            hd_cats = [c for c in categories_list if "hợp đồng" in c.lower()]
            if hd_cats:
                suggested_category = hd_cats[0]
        elif "tờ trình" in combined_text or "tt" in combined_text:
            tt_cats = [c for c in categories_list if "tờ trình" in c.lower()]
            if tt_cats:
                suggested_category = tt_cats[0]
        elif categories_list:
            suggested_category = categories_list[0]

    # Mô phỏng gợi ý nhân viên dựa trên tên xuất hiện trong văn bản
    for emp in employees:
        emp_name_lower = emp.ho_va_ten.lower()
        # Tìm theo họ tên đầy đủ hoặc tên riêng
        if emp_name_lower in combined_text or (emp.ten and emp.ten.lower() in combined_text):
            suggested_employee = emp.ho_va_ten
            break
            
    if not suggested_employee and employees_list:
        suggested_employee = employees_list[0]

    # Mô phỏng tóm tắt văn bản
    summary = f"[MÔ PHỎNG AI] Văn bản hành chính có tiêu đề '{title}'. "
    if content:
        summary += f"Nội dung xoay quanh việc: {content[:100]}... "
    summary += "Đề nghị đơn vị và cá nhân được phân công xử lý nhanh chóng hoàn thiện hồ sơ."

    mock_response = {
        "category": suggested_category,
        "employee": suggested_employee,
        "summary": summary
    }
    
    status = "mock" if not api_key else "fallback"
    return mock_response, status
