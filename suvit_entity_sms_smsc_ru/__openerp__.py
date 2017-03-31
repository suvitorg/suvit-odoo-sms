{
    'name': "Suvit smsc.ru",
    'version': "1.0",
    'author': "SUVIT LLC",
    'category': "Tools",
    'summary': "Allows 2 way sms conversations between leads/partners using the smsc.ru gateway",
    'license':'LGPL-3',
    'data': [
        # 'security/ir.model.access.csv',

        'data/esms.gateways.csv',

        'views/gateway_config.xml',
    ],
    'demo': [],
    'depends': [
        'entity_sms'
    ],
    'images':[
    ],
    'installable': True,
    'application': True,
}