# Paste Parser

Simple Python module for parsing Pokepastes. The syntax is outlined here: https://pokepast.es/syntax.html

## Installing

```
pip install git+https://github.com/mikewVGC/paste-parser.git
```

## Usage

```
from paste_parser.paste_parser import PasteParser

parser = PasteParser()

with open("your/pokepaste/file", 'r') as pastefile:
    mons = parser.parse(pastefile.read())
```

`mons` will be a list of `Pokemon` which is a simple dataclass.

## Build The Module

To build the module:

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python setup.py sdist bdist_wheel
```

## Testing

To run the very small amount of unit tests:

```
python -m unittest discover -v
```

## License

Paste Parser is licensed with the BSD license. See `LICENSE`.
