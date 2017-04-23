from openerp import models, fields, api

def is_cellular(phone):
    # test phone for '9XXXXXXXXX' format
    return phone and phone.isdigit() and len(phone) == 10 and phone[0] == '9'


class Partner(models.Model):
    _inherit = "res.partner"

    sms_track = fields.Boolean(string="Получать смс-рассылку",
                               default=True,
                               help="Если да, пользователь получает sms, если нет - не получает",
                               )

    @api.one
    @api.depends('country_id', 'mobile', 'phone')
    def _calc_e164(self):
        norm_phone = self.mobile or self.phone or ''

        # normalize mobile_e164
        if not norm_phone:
            return

        norm_phone = norm_phone.translate(None, "()- ")
        if len(norm_phone) < 10:
            # too few digits, may be without city number
            return

        if norm_phone.startswith("+"):
            # norm_phone = self.mobile[1:]
            pass
        elif self.country_id.mobile_prefix:
            if norm_phone.startswith("0"):
                norm_phone = self.country_id.mobile_prefix + self.mobile[1:]
            else:
                norm_phone = self.country_id.mobile_prefix + norm_phone

        # check on cellular ?
        self.mobile_e164 = norm_phone


class Lead(models.Model):
    _inherit = 'crm.lead'
    _calc_e164 = Partner._calc_e164.im_func
