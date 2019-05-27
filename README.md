# DBISAM to JSON

This is a small tool written in python to extract database values from .dat files programmatically. I couldn't find any tools on the web to do so, so I wrote one myself.
Currently it can read the following fields:

- Varchar
- Int
- Float
- Date

## Usage

```
usage: convert.py [-h] [-j] [-c CSV] [-o OUT] [-s] filename

converts a DBISAM .dat file to JSON format

positional arguments:
  filename           the .dat file you want to extract data from

optional arguments:
  -h, --help         show this help message and exit
  -j, --json         print output in JSON format
  -c CSV, --csv CSV  create a csv file containing the output
  -o OUT, --out OUT  instead of printing to stdout, save data to file.
  -s, --stream       print data row by row while it's being read

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
```

Stream the data to stdout (print row by row)
```
python convert.py <filename> -s
```

## Dependencies

This script is originally written in python 2.7. A version that runs in python3 van be found in the python3 folder.
