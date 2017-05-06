# -*- coding: utf-8 -*-
import pytz

from openerp import api, fields, models
from openerp.http import request

from openerp.addons.entity_sms.esms_templates import mako_template_env

def user_datetime(date_str):
    if request:
        env = request.env
        user_tz = pytz.timezone(env.context.get('tz') or env.user.tz or 'UTC')
    else:
        user_tz = pytz.utc

    return user_tz.localize(fields.Datetime.from_string(date_str)).astimezone(pytz.utc)


def ru_date_format(dt):
    return dt.strftime('%d.%m.%Y')

mako_template_env.filters.update(user_datetime=user_datetime,
                                 ru_date_format=ru_date_format)


class EsmsTemplate(models.Model):
    _inherit = "esms.templates"

    # dont use translation on template
    template_body = fields.Text(translate=False)
