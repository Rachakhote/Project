# -*- coding: utf-8 -*-

{
    'name': "Vehicle Module",
    'version': '1.0',
    'depends': ['base', 'fleet'],
    'author': "Author Name",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/vehicle_management.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'application': True,
}
