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
        'security/groups.xml',
        'data/sequence.xml',
        'report/report.xml',
        'views/form.xml',
        'views/tree.xml',
        'views/kanban.xml',
        'views/calendar.xml',
        'views/search.xml'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True
}

