# DBISAM to JSON

This is a small tool written in python because I needed to extract database values from .dat files programmatically and couldn't find any tools on the internet to do so.
Currently it can read the following fields:

- Varchar
- Int
- Float
- Date

## Usage

```
read.py [-h] [-j] [-c] [-o OUT] filename

converts a DBISAM .dat file to JSON format

positional arguments:
  filename           the .dat file you want to extract data from

optional arguments:
  -h, --help         show this help message and exit
  -j, --json         print output in JSON format
  -c, --csv          print output in CSV format
  -o OUT, --out OUT  instead of printing to stdout, save data to file.

```

Will print the file's records in JSON format
