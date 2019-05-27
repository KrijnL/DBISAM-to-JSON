# DBISAM to JSON

This is a small tool written in python because I needed to extract database values from .dat files programmatically and couldn't find any tools on the internet to do so.
Currently it can read the following fields:

- Varchar
- Int
- Float
- Date

## Usage

```
convert.py [-h] [-j] [-c] [-o OUT] filename

converts a DBISAM .dat file to JSON format

positional arguments:
  filename           the .dat file you want to extract data from

optional arguments:
  -h, --help         show this help message and exit
  -j, --json         print output in JSON format
  -c, --csv          print output in CSV format
  -o OUT, --out OUT  instead of printing to stdout, save data to file.

```

The following will print the file's records to stdout in JSON format:
```
python convert.py <filename>
```

The following exports to a csv file:
```
python convert.py <filename> -c outfile.csv
```

This will export to a JSON file:
```
python convert.py <filename> -o outfile.json

## Dependencies

This script is written in python 2.7, it will not work in python 3.x.
Porting to python 3 issomething I might do in the future, but for now it works...
