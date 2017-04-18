# -*- coding: utf-8 -*-
from openerp import api, fields, models


class SmsTracker(models.AbstractModel):
    """
        Use:
        class Order(models.Model):
            _name = 'sale.order'
            _inherit = ['sale.order',
                        'suvit.sms.tracker']
            _sms_track_fields = ['state']
    """
    _name = 'suvit.sms.tracker'

    _sms_track_fields = []

    @api.multi
    def write(self, vals):
        res = super(SmsTracker, self).write(vals)

        changed_sms_fields = set(self._sms_track_fields) & set(vals)
        if not changed_sms_fields:
            return res

        for sms_track_field in changed_sms_fields:
            # found sms template, for example 'sale.order_state_sent'
            template_name = '%s_%s_%s' % (self._name,
                                          sms_track_field,
                                          vals[sms_track_field]
                                          )

            template = self.env['esms.templates'].search([('name', '=', template_name),
                                                          ('model', '=', self._name)],
                                                         limit=1)
            if not template:
                continue

            # send sms template
            for rec in self:
                if not getattr(rec, 'sms_track', True):
                    # dont sent for partner/order with disable sms_track
                    continue
                template.send_template(template.id, rec)

        return res
