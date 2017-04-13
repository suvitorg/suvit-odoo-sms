# -*- coding: utf-8 -*-
from openerp import api, fields, models


class SmsHandler(models.Model):
    _name = 'suvit.sms.handler'
    _descripion = u'Обработчик шлюза Шлюз SMSЦентр'
    _order = 'sequence,id'

    name = fields.Char(string=u'Название обработчика',
                       track_visibility='onchange'
                       )

    sequence = fields.Integer(string=u'Порядок',
                              default=99,
                              track_visibility='onchange')

    active = fields.Boolean(string=u'Активный',
                            default=True,
                            track_visibility='onchange')

    direction = fields.Selection(string=u'Направление',
                                 selection=[('I', u'Входящие'),
                                            ('O', u'Исходящие')],
                                 track_visibility='onchange'
                                 )

    method = fields.Char(string=u'Имя метода',
                         track_visibility='onchange')

    @api.constrains('method')
    def check_method(self):
        if not hasattr(self, self.method):
            raise exceptions.ValidationError(u"Неправильное имя обработчика %s" % self.method)

    @api.multi
    def run(self, sms):
        # sms is dict with keys:
        #  'direction' - 'I', 'O'
        #  'id' - ИД. наверно, только для входящих
        #  'from_number' - откого
        #  'to_number' - накакой номер
        #  'data' - дата
        #  'body' - сообщение
        #  'cost' - цена (Decimal)
        # handler can change sms dict
        self.ensure_one()
        handler = getattr(self, self.method)
        return handler(sms)

    @api.model
    def run_all(self, sms):
        domain = []

        direction = sms.get('direction')
        if direction:
            domain.append(('direction', '=', direction))

        for handler in self.search(domain):
            handler.run(sms)
