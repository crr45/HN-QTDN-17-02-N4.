# -*- coding: utf-8 -*-
from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    gemini_api_key = fields.Char(
        string="Gemini API Key",
        config_parameter='gemini_api_key',
        help="Google Gemini API Key for AI document analysis and chatbot."
    )
