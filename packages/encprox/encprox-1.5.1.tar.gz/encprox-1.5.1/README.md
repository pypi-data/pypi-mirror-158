# srcbpy
A simple python library for formatting proxies.

# Installation
```
pip install encprox
```

# Usage
```py
from encprox import prox
api = prox()
print(api.proxy_format('file_path')) # You don't need to do open file code, just type the file path and it will automatically read it.
```