# -*- coding: utf-8 -*-
from openerp import api, fields, models


class EsmsTemplate(models.Model):
    _inherit = "esms.templates"

    template_body = fields.Text(translate=False)
