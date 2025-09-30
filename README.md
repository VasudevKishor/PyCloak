# PyCloak

**A powerful and modern obfuscator for Python source code.**


> ** Project Status: Under Heavy Development **
>
> PyCloak is currently in an early development phase. The API is subject to change.

PyCloak is a command-line tool designed to protect your Python intellectual property by transforming readable source code into a functionally identical but difficult-to-understand format. It uses advanced techniques based on Python's Abstract Syntax Tree (AST) to provide robust obfuscation.

## Key Features

* **Name Mangling:** Intelligently renames variables, functions, and classes to short, meaningless names.
* **String Encryption:** Encrypts string literals to hide sensitive data and messages.
* **Control Flow Flattening:** Restructures the code's logic into a complex state machine, making it extremely difficult to follow.
* **Bundling Support:** Designed to work with tools like **PyInstaller** to package your obfuscated code into a single executable.

## Installation

As the project is under development, it is not yet available on PyPI. To install it, clone the repository directly:

```bash
git clone [https://github.com/your-username/pycloak.git](https://github.com/vasudevkishor/pycloak.git)
cd pycloak
pip install .
```

## Usage

PyCloak is used via its command-line interface. The most basic usage is to provide a source directory and an output directory.

```bash
pycloak --source ./my_project --output ./dist
```

### Example

**Before Obfuscation (`my_project/main.py`):**
```python
class Calculator:
    def add(self, num1, num2):
        result = num1 + num2
        print(f"The result is: {result}")
        return result

if __name__ == "__main__":
    calc = Calculator()
    calc.add(10, 20)
```

**After Obfuscation (`dist/main.py`):**
```python
import base64
_d = ['VGhlIHJlc3VsdCBpczoge30=']
def _x(i): return base64.b64decode(_d[i]).decode()

class _a:
    def _b(self, _c, _d):
        _e = 0
        while True:
            if _e == 0:
                _f = _c + _d
                _e = 1
            elif _e == 1:
                print(_x(0).format(_f))
                _e = 2
            elif _e == 2:
                return _f

if __name__ == '__main__':
    _g = _a()
    _g._b(10, 20)
```

## Disclaimer

Obfuscation is a deterrent, not a foolproof security measure. A determined and skilled attacker can still reverse-engineer the code. PyCloak is intended to protect against casual inspection and to significantly raise the bar for reverse-engineering. This tool should be used for protecting legitimate intellectual property and not for creating malware.


## Contributing

Contributions, issues, and feature requests are welcome!
