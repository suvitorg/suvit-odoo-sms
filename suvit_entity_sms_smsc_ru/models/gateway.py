# -*- coding: utf-8 -*-
import datetime
import hashlib

import requests

from openerp import api, fields, models


class SmscResponse:
    delivary_state = ""
    response_string = ""
    human_read_error = ""
    message_id = ""


def format_number(number):
    number = number.replace(" ", "")
    number = number.replace("+", "")
    return number


class SmscGateway(models.Model):
    _name = 'esms.smsc'
    _descripion = u'Шлюз SMSЦентр'

    _api = None

    ERRORS = [
        (1, u'Ошибка в параметрах.'),
        (2, u'Неверный логин или пароль.'),
        (3, u'Недостаточно средств на счете Клиента.'),
        (4, u'IP-адрес временно заблокирован из-за частых ошибок в запросах'),
        (5, u'Неверный формат даты.'),
        (6, u'Сообщение запрещено (по тексту или по имени отправителя).'),
        (7, u'Неверный формат номера телефона.'),
        (8, u'Сообщение на указанный номер не может быть доставлено.'),
        (9, u'Отправка более одного одинакового запроса на передачу SMS-сообщения'
            u' либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты.'),
    ]

    def send_message(self, account_id,
                     from_number, to_number, sms_content,
                     my_model_name='', my_record_id=0, my_field_name=''):

        sms_account = self.env['esms.accounts'].search([('id', '=', account_id)])
        gateway_id = self.env['esms.gateways'].search([('gateway_model_name', '=', 'esms.smsc')])

        from_number = format_number(from_number)
        to_number = format_number(to_number)

        try:
            resp = requests.post('http://smsc.ru/sys/send.php',
                                 data={'login': sms_account.smsc_username,
                                       'psw': hashlib.md5(sms_account.smsc_password).hexdigest(),
                                       'sender': from_number,
                                       'phones': to_number,
                                       'mes': sms_content,
                                       'charset': 'utf-8', # always use utf8
                                       'cost': 2,  # обычная отправка, но добавить в ответ стоимость выполненной рассылки
                                       'fmt': 3,  # ответ в json формате
                                       })
        except:
            # TODO timeout errors
            pass

        # resp format. json
        # {
        # "id": <id сообщения>,
        # "cnt": n,
        # "cost": "cost",
        # "error": "описание",
        # "error_code": N,
        # }
        resp_dict = resp.json()

        status = 'successful'
        human_read_error = 'OK'
        if 'error_code' in resp_dict:
            status = 'failed'
            human_read_error = resp_dict.get('error')

        sms_id = resp_dict.get('id', 0)
        cost = resp_dict.get('cost', 0)

        # status code
        # ('RECEIVED','Received'),
        # ('failed', 'Failed to Send'),
        # ('queued', 'Queued'),
        # ('successful', 'Sent'),
        # ('DELIVRD', 'Delivered'),
        # ('EXPIRED','Timed Out'),
        # ('UNDELIV', 'Undelivered'))
        my_model = self.env['ir.model'].search([('model','=', my_model_name)])
        my_field = self.env['ir.model.fields'].search([('model_id', '=', my_model.id),
                                                       ('name', '=', my_field_name)])

        history_id = self.env['esms.history'].create({'account_id': sms_account.id,
                                                      'gateway_id': gateway_id.id,

                                                      'status_code': status,
                                                      'status_string': human_read_error,
                                                      'delivary_error_string': human_read_error,

                                                      'from_mobile': from_number,
                                                      'to_mobile': to_number,
                                                      'sms_gateway_message_id': sms_id,
                                                      'sms_content': sms_content,
                                                      'direction': 'O',
                                                      'my_date': datetime.datetime.utcnow(),

                                                      'model_id': my_model.id,
                                                      'record_id': my_record_id,
                                                      'field_id': my_field.id,

                                                      'cost': cost})

        my_sms_response = SmscResponse()
        my_sms_response.delivary_state = status
        my_sms_response.response_string = resp.text
        my_sms_response.human_read_error = human_read_error
        my_sms_response.message_id = sms_id
        return my_sms_response

    def check_messages(self, account_id, message_id=""):
        sms_account = self.env['esms.accounts'].browse(account_id)
        gateway_id = self.env['esms.gateways'].search([('gateway_model_name', '=', 'esms.smsc')])

        # receive. GET or POST
        # http://smsc.ru/sys/get.php?get_answers=1&login=<login>&psw=<password>

        # TODO. check for one message
        if message_id != "":
            pass
        else:
            pass

        request_data = {'get_answers': 1,
                        'login': sms_account.smsc_username,
                        'psw': hashlib.md5(sms_account.smsc_password).hexdigest(),
                        'fmt': 3,  # json format
                        }

        if sms_account.smsc_store_last_received_id and sms_account.smsc_last_received_id:
            request_data['after_id'] = sms_account.smsc_last_received_id

        # get all messages
        resp = requests.post('http://smsc.ru/sys/get.php',
                             data=request_data)

        # resp error
        # {
        # "error": "описание",
        # "error_code": N
        # }
        # Значение	Описание
        # 1	Ошибка в параметрах.
        # 2	Неверный логин или пароль.
        # 4	IP-адрес временно заблокирован.
        # 9	Попытка отправки более трех одинаковых запросов на получение списка входящих сообщений в течение минуты.

        # resp ok
        # [{
        #  "id": <id>,
        #  "received": "<received>",
        #  "phone": "<phone>",
        #  "message": "<message>",
        #  "to_phone": "<to_phone>",
        #  "sent": "<sent>"
        #  },
        #  ...]

        resp_data = resp.json()
        if 'error_code' in resp_data:
            # TODO. store error in history
            status = 'failed'
            human_read_error = resp_data['error']
            return

        sms = None
        for sms in resp_data:
            status = 'RECEIVED'
            human_read_error = 'OK'
            history_id = self.env['esms.history'].create({'account_id': sms_account.id,
                                                          'gateway_id': gateway_id.id,

                                                          'status_code': status,
                                                          'status_string': human_read_error,
                                                          'delivary_error_string': human_read_error,

                                                          'from_mobile': sms.phone,
                                                          'to_mobile': sms.to_phone,
                                                          'sms_gateway_message_id': sms.id,
                                                          'sms_content': sms.message,
                                                          'direction': 'I',
                                                          'my_date': sms.received,
                                                          # 'model_id': my_model.id,
                                                          # 'record_id': my_record_id,
                                                          # 'field_id': my_field.id,
                                                          'cost': 0  # ???
                                                          })

            continue

            # Custom logic, this may be pluggable
            # 
            target_model = 'sale.order' # or lead
            record_id = 1
            self.env[target_model].search([('id', '=', record_id)]).message_post(body=sms.message,
                                                                                 subject="Получено SMS")

        if sms_account.smsc_store_last_received_id and sms:
            sms_account.smsc_last_received_id = sms.id


class SmscAccount(models.Model):
    _inherit = "esms.accounts"

    smsc_username = fields.Char(string='SMSЦентр API Username')
    smsc_password = fields.Char(string='SMSЦентр API Пароль')
    # smsc_sender = fields.Char(string=u'SMSЦентр API Отправитель') - use esms.verified.numbers

    smsc_store_last_received_id = fields.Boolean(string=u'Сохранять последний полученный ид')
    smsc_last_received_id = fields.Integer(string=u'Последний полученный ид')
