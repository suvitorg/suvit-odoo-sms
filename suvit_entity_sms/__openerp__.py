{
    'name': "Suvit SMS",
    'version': "1.0",
    'author': "SUVIT LLC",
    'website': 'https://suvit.ru',
    'category': "Tools",
    'summary': "Allows send sms from entity_sms module",
    'license':'LGPL-3',
    'depends': [
        'entity_sms'
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/handler.xml',
        'views/history.xml',
    ],
    'demo': [],
    'images':[
    ],
    'installable': True,
    'application': False,
}
