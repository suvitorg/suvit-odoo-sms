# -*- coding: utf-8 -*-
from openerp import api, fields, models

API_URL = 'http://95.213.129.83/xml/'


login_tpl = '<?xml version="1.0" encoding="utf-8"?><request><security><login value="{login}" /><password value="{password}" /></security></request>'

send_tpl = """<?xml version="1.0" encoding="utf-8" ?>
<request>
  <security>
    <login value="{login}" />
    <password value="{password}" />
  </security>
  <message type="sms">
    <sender>{sender}</sender>
    <text>{body}</text>
    <abonent phone="{to_number}" number_sms="1" client_id_sms="{sms_id_todo}" time_send="" />
  </message>
</request>
""".replace('\n', '')

class P1SmsResponse:
    error = ''
    information = ''


class P1Gateway(models.Model):
    _name = 'esms.p1'
    _descripion = u'Шлюз P1 SMS'

    def send_sms(self, sms_gateway_id,
                 to_number, sms_content,
                 my_model_name, my_record_id, my_field_name):
        pass

    def check_messages(self, account_id, message_id=""):
        pass


class P1Account(models.Model):
    _inherit = "esms.accounts"

    p1sms_username = fields.Char(string='P1 API Usernname')
    p1sms_password = fields.Char(string='P1 API Пароль')
    # p1_api_id = fields.Char(string='P1 API ID')
    p1sms_sender = fields.Char(string=u'P1 API Отправитель')
