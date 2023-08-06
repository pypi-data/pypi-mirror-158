# file2
A python module to read or write to compressed or uncompressed files.
Similar to the `open` function, this provides a single function call for opening files using standard modules build in to python3.

## Installation
To install in python3:
`pip install file2`

## Usage
```python
from file2 import fopen
with fopen(filename, mode='rt', *args, **kwargs)
```

`fopen` will infer the file type based on the extension:

|Ext|File Type|Returns|
|---|---|---|
|.gz|gzip|[GzipFile](https://docs.python.org/3/library/gzip.html)
|.bz2|bzip2|[BZ2File](https://docs.python.org/3/library/bz2.html)
|.xz|xz/lzma|[LZMAFile](https://docs.python.org/3/library/lzma.html)
|.*|uncompressed|[file object](https://docs.python.org/3/library/functions.html#open)

The available modes depend on the file type.
`fopen` passes the mode directly to the specific opener without modification.
