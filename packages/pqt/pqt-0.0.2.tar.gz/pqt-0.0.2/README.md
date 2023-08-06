# parquet-tools

`pqt` is a command line interface tool for analyzing parquet quickly. `pqt` makes use of 
[duckdb](https://github.com/duckdb/duckdb) to quickly analyze parquet files. 

### How to install

`pqt` is an easy-to-install package, which can be installed with `pip` from PyPi:

`pip install pqt`

### Supported functionalities:

+ `pqt.head example.parquet` prints the first `n` (default: 10) rows of the parquet file `example.parquet`.
    + You can use the `-n` or `--lines` flag to change the number of rows to print.

+ `pqt.tail example.parquet` prints the last `n` (default: 10) rows of the parquet file `example.parquet`.
    + You can use the `-n` or `--lines` flag to change the number of rows to print.