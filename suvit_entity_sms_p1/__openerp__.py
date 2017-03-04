{
    'name': "Suvit P1 SMS",
    'version': "1.0",
    'author': "SUVIT LLC",
    'category': "Tools",
    'summary': "Allows 2 way sms conversations between leads/partners using the p1sms gateway",
    'license':'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/gateway_config.xml',
    ],
    'demo': [],
    'depends': [
        'entity'
    ],
    'images':[
    ],
    'installable': True,
    'application': True,
}