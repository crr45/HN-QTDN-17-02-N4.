# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        # 1. Gọi hàm gốc để thực hiện xác nhận đơn hàng (nó sẽ tự động tạo Phiếu xuất kho stock.picking thông qua Odoo Stock)
        res = super(SaleOrder, self).action_confirm()
        _logger.info(">>> EVENT TRIGGERED: Sale Order %s has been confirmed. Executing automated workflow...", self.name)
        
        # 2. Tự động hóa: Tạo Hóa đơn (account.move) và Ghi sổ (action_post -> đẩy bút toán vào Sổ cái)
        for order in self:
            try:
                if order.invoice_status == 'to invoice':
                    _logger.info(">>> AUTOMATION: Creating Invoice for Order %s", order.name)
                    # Gọi API để sinh hóa đơn
                    invoice = order._create_invoices()
                    if invoice:
                        _logger.info(">>> AUTOMATION: Posting Invoice %s (adding entry to General Ledger)", invoice.name)
                        # Ghi sổ hóa đơn (Post invoice to General Ledger)
                        invoice.action_post()
            except Exception as e:
                _logger.error(">>> AUTOMATION ERROR: Failed to automatically invoice/post order %s: %s", order.name, str(e))
        
        return res
