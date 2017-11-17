# Transmathematics for Python

A Python module which makes division by zero possible.

_Please note: it is a known bug that (-1).root(2) returns nullity, instead of a transcomplex number. This is because transcomplex numbers have not yet been implemented in this module._

## Installation

### From PyPI

Coming soon...

### From GitHub

`pip3 install git+https://github.com/BenjaminEHowe/python-transmaths.git`

## Usage

```python
import transmaths

transmaths.Transreal(1) # create a transreal number representing 1
transmaths.Transreal(1, 3) # create a transreal number representing one third
transmaths.Transreal(1/3) # create a transreal number representing floating point one third (6004799503160661/18014398509481984)
transmaths.Transreal(64).root(3) # calculate the third root of 64 (exactly 4, not 3.9999999999999996 as `64**(1/3)` would have you believe)
transmaths.Transreal(2).root(2) # calculate the (approximate) square root of 2
```
