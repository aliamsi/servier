# Exemple de SCHEMA où chaque colonne a un nom et un type attendu
# SCHEMA = {
#     'drugs': {
#         'columns_and_types' : {
#             'atccode': str,
#             'drug': str
#         },
#         'not_nullable': [
#             'atccode',
#             'drug'
#         ]
#     },
#     'clinical_trials': {
#         'columns_and_types': {
#             'id': str,
#             'scientific_title': str,
#             'date': str,
#             'journal': str
#         },
#         'not_nullable': [
#             'id',
#             'date'
#         ]
#     },
#     'pubmed': {
#         'columns_and_types': {
#             'id': int,
#             'title': str,
#             'date': str,
#             'journal': str
#         },
#         'not_nullable': [
#             'id',
#             'date'
#         ]
#     },
#     'search_column': {
#         'drugs': 'drug',
#         'clinical_trials': 'scientific_title',
#         'pubmed': 'title'
#     }
    
# }

SCHEMA = {
    'drugs': {
        'atccode': str,
        'drug': str
    },
    'clinical_trials': {
        'id': str,
        'scientific_title': str,
        'date': str,
        'journal': str
    },
    'pubmed': {
        'id': int,
        'title': str,
        'date': str,
        'journal': str
    },
    'search_column': {
        'drugs': 'drug',
        'clinical_trials': 'scientific_title',
        'pubmed': 'title'
    }
}