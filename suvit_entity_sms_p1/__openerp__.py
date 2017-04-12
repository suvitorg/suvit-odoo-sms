{
    'name': "Suvit P1 SMS",
    'version': "1.0",
    'author': "SUVIT LLC",
    'website': 'https://suvit.ru',
    'category': "Tools",
    'summary': "Allows 2 way sms conversations between leads/partners using the p1sms.ru gateway",
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
    "external_dependencies": {
        'python': ['requests',
                   ]
    },
    'images':[
    ],
    'installable': False,  # not work yet
    'application': True,
}