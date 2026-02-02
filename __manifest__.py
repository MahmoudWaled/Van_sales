{
    'name': 'Egyptian Van Sales System',
    'version': '19.0.0.1.0',
    'category': 'Sales',
    'summary': 'Manage Van Sales, Routes, and Commissions for Egypt Market',
    'depends': ['sale_management', 'stock', 'account', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_view.xml',
        'views/van_route_view.xml',
        'views/hr_employee_view.xml',
    ],
    'installable': True,
    'application': True,
}
