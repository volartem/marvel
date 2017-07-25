{
    'name': 'Comics Marvel API',
    'description': 'See comics from Marvel',
    'author': 'VolArtem',
    'depends': ['website'],
    'application': True,
    'summary': 'Module that allow to view comics from Marvel',
    'version': ' 1.0.',
    'license':  'LGPL-3',
    'category': 'API',
    'data': [
        'views/menu.xml',
        'views/templates.xml',
    ],
    'qweb': ['static/src/xml/project_button.xml',
             'static/src/xml/qwebtemplate.xml',
    ],
}
