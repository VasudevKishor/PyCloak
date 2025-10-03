import base64
_e = ['VmFzdWRldg==', 'X19tYWluX18=']

def _d(i):
    return base64.b64decode(_e[i]).decode('utf-8')
from utils import _SuPn, _nKaT

def _TiJc():
    user_id = _nKaT()
    print(f'User ID: {user_id}')
    formatter = _SuPn()
    greeting = formatter._bKQp(_d(0))
    print(greeting)
if __name__ == _d(1):
    _TiJc()