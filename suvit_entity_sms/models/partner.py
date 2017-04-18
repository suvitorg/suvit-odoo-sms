from openerp import models, fields, api


class Partner(models.Model):
    _inherit = "res.partner"

    sms_track = fields.Boolean(string="Получать смс-рассылку",
                               default=True,
                               help="Если да, пользователь получает sms, если нет - не получает",
                               )
