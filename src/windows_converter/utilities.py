# """Utilities for Windows converter."""
# import platform
# from pathlib import Path


# _geometries = {
#     'frm_main': {
#         'Linux': '500x600',
#         'Windows': '500x600',
#     },
#     'frm_project': {
#         'Linux': '900x650',
#         'Windows': '700x600',
#     },
#     'frm_config': {
#         'Linux': '700x300',
#         'Windows': '700x300',
#     },
# }
# system = platform.system()
# if system not in ['Linux', 'Windows']:
#     system = 'Linux'


# def geometry(form: str = '') -> str:
#     return _geometries[Path(form).stem][system]
