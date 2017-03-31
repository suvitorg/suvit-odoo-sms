# -*- coding: utf-8 -*-
from openerp import api, fields, models

class EsmsHistory(models.Model):
    _inherit = "esms.history"

    cost = fields.Float(string=u'Цена',
                        digits=(2, 2),
                        readonly=True)
