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
        'data/sequence.xml',
        'views/vehicle_management_form.xml',
        'views/vehicle_management_tree.xml',
        'views/vehicle_management_kanban.xml',
        'views/vehicle_management_calendar.xml',
        'views/vehicle_management_pivot.xml',
        'views/vehicle_management_search.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'application': True,
}
